from flask import render_template, redirect, url_for, session, flash, request
from flask_login import login_user, login_required, fresh_login_required, current_user
from flask_mail import Message
from sqlalchemy import or_, desc

from .extensions import db, bc, timedSerializer, mail
from .forms import CSVUpload, UserLogin, UserRegister, ChangePassword, Search
from .models import Student, Guest, User_
from .scripts import checkString, checkInt, checkBool, checkCash


def index():
    return redirect(url_for("main.home"))


def login():
    form = UserLogin()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid email/password", "warn")
        return render_template("main/login.html", form=form)

    user = db.session.query(User_).filter_by(email=form.email.data.lower()).first()

    if not user:
        flash("User does not exist", "info")
        return render_template("main/login.html", form=form)
    elif not user.verified:
        flash("Please confirm your email", "warn")
        return render_template("main/login.html", form=form)
    elif not bc.check_password_hash(user.password, form.password.data):
        flash("Incorrect password!", "danger")
        return render_template("main/login.html", form=form)

    login_user(user, remember=form.remember.data)
    flash("Logged in successfully!", "success")

    if "next" in session:
        next_val = session["next"]
        if next_val.split("/")[1] != "action":
            return redirect(next_val)

    return redirect(url_for("main.home"))


@login_required
def home():
    return render_template("main/home.html")


@login_required
def search():
    form = Search()
    if not form.validate_on_submit():
        if "returnLog" in session and "search" in session:
            form.query.data = session.get("search")
            session.pop("returnLog")
        else:
            if "search" in session:
                session.pop("search")
            if len(form.errors) != 0:
                flash("Invalid input", "warn")
            return render_template("main/search.html", form=form)

    session["search"] = form.query.data
    students = []
    guests = []
    try:
        query = int(form.query.data)
        students = Student.query.filter(or_(Student.ticket_num == query, Student.school_id == query)).all()

        guests = Guest.query.filter_by(ticket_num=query).all()
    except ValueError:
        query = form.query.data.title()

        students = Student.query.filter(or_(Student.first_name == query, Student.last_name == query)).all()
        guests = Guest.query.filter(or_(Guest.first_name == query, Guest.last_name == query)).all()

    finally:
        for i in students:
            for j in i.guests:
                guests.append(j)

    return render_template("main/search.html", form=form, students=students, guests=guests)


@fresh_login_required
def register():
    form = UserRegister()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid email/password", "warn")
        return render_template("main/register.html", form=form)

    user_search = User_.query.filter_by(email=form.email.data).first()
    if user_search:
        if user_search.verified:
            flash("Email already registered", "info")
            return render_template("main/register.html", form=form)
        else:
            db.session.delete(user_search)
            db.session.commit()

    if form.password.data != form.confirmPassword.data:
        flash("Passwords do not match", "danger")
        return render_template("main/register.html", form=form)

    user = User_(form.email.data.lower(), form.password.data, False)
    db.session.add(user)
    db.session.commit()

    confirm_email = Message("Event Check In Email Confirmation",
                            sender="Event Check In",
                            recipients=[form.email.data])

    confirm_email.html = render_template("email/confirmEmail.html",
                                         token=timedSerializer.dumps(form.email.data,
                                                                     salt="emailConfirm"))
    mail.send(confirm_email)

    flash("Email verification sent, please confirm your email", "success")
    return redirect(url_for("main.login"))


@login_required
def upload():
    form = CSVUpload()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid File Type", "danger")
        return render_template("main/upload.html", form=form)

    # Read and parse CSV Data
    rawData = form.csvData.data.read().decode().split('\n')

    parsedData = [i.strip('\r').split(',') for i in rawData]
    if parsedData[0] != ["Ticket", "ID", "LAST", "MI", "FIRST", "GR", "Payment Method", "Guest YN", "Guest Ticket "
                                                                                                    "Number"]:
        flash("Invalid CSV", "danger")
        return render_template("main/upload.html", form=form)

    del parsedData[0]

    # Clear the Student and Guest tables
    db.session.execute(Guest.__table__.delete())
    db.session.execute(Student.__table__.delete())
    db.session.commit()

    # Store the attendees in the database
    guest_ids = {}
    guests = []
    for user in parsedData:
        if user[7] == "Y":
            guest_ids[user[8]] = user[1]  # [guest_id : host_school_id]

    for user in parsedData:
        user_id = user[0]
        if user_id in guest_ids.keys():
            guests.append([user, guest_ids[user_id]])
        else:
            is_cash, check_num = checkCash(user[6])

            student = Student(checkInt(user[0]), checkInt(user[1]), checkString(user[4]), checkString(user[2]), is_cash,
                              check_num, checkBool(user[7]))

            db.session.add(student)

    for user, host_school_id in guests:
        is_cash, check_num = checkCash(user[6])
        guest = Guest(checkInt(user[0]), host_school_id, checkString(user[4]), checkString(user[2]), is_cash, check_num)

        db.session.add(guest)

    db.session.commit()
    flash("File Successfully Uploaded!", "success")
    return render_template("main/upload.html", form=form)


@login_required
def attendees():
    stu_filters = {"first_name": Student.first_name, "last_name": Student.last_name, "ticket_num": Student.ticket_num,
                   "school_id": Student.school_id}
    guest_filters = {"first_name": Guest.first_name, "last_name": Guest.last_name, "ticket_num": Guest.ticket_num}

    page = request.args.get("page", 1)
    order = request.args.get("filter", "ticket_num")
    is_desc = request.args.get("desc") == "True"
    guests = request.args.get("guests") == "True"

    if guests:
        order = guest_filters.get(order, Student.ticket_num)
    else:
        order = stu_filters.get(order, Student.ticket_num)

    order = desc(order) if is_desc else order
    group = db.session.query(Guest if guests else Student).order_by(order).all()

    chunkSize = 25
    chunks = len(group) // chunkSize + 1

    try:
        page = int(page)
        page = page if page in range(1, chunks + 1) else 1
    except ValueError:
        page = 1

    listEnd = chunkSize * page

    return render_template("main/attendees.html", group=group[listEnd - chunkSize:listEnd], chunks=chunks,
                           guests=guests)


@fresh_login_required
def settings():
    form = ChangePassword()
    if not form.validate_on_submit():
        ...
    elif not bc.check_password_hash(current_user.password, form.currentPassword.data):
        flash("Incorrect password", "danger")
    elif form.newPassword.data != form.confirmNewPassword.data:
        flash("Passwords don't match", "danger")
    else:
        current_user.changePassword(form.newPassword.data)
        db.session.commit()
        return redirect(url_for("action.logout"))

    return render_template("main/settings.html", form=form)


def helpPage():
    return "Help"
