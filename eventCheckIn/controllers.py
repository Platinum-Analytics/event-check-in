from flask import render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

from .extensions import db, bc
from .forms import CSVUpload, UserLogin, UserRegister
from .models import Student, Guest, User_
from .scripts import checkString, checkInt, checkBool, checkCash


def index():
    return redirect(url_for("main.login"))


def login():
    form = UserLogin()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid Username/Password", "warn")
        return render_template("login2.html", form=form)

    user = User_.query.filter_by(username=form.username.data).first()

    if not user:
        flash("User does not exist!", "info")
        return render_template("login2.html", form=form)
    elif not bc.check_password_hash(user.password, form.password.data):
        flash("Incorrect Password!", "danger")
        return render_template("login2.html", form=form)

    login_user(user)
    flash("Logged In Successfully!", "success")

    if "next" in session:
        nextVal = session["next"]
        if nextVal != "/logout":
            return redirect(nextVal)

    return render_template("home.html")


@login_required
def home():
    return render_template("home.html")


@login_required
def register():
    form = UserRegister()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid Username/Password", "warn")
        return render_template("register.html", form=form)

    if not bc.check_password_hash(current_user.password, form.currentPassword.data):
        flash("Incorrect password!", "danger")
        return render_template("register.html", form=form)

    newUser = User_(form.username.data, form.password.data)

    try:
        db.session.add(newUser)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("That username already exists!", "info")
        return render_template("register.html", form=form)

    flash("Successfully Registered!", "success")
    return redirect(url_for("main.login"))


@login_required
def logout():
    logout_user()
    flash("Successfully logged out!", "success")
    return redirect(url_for("main.login"))


@login_required
def upload():
    form = CSVUpload()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid File Type", "danger")
        return render_template("upload.html", form=form)

    # Read and parse CSV Data
    rawData = form.csvData.data.read().decode().split('\n')

    parsedData = [i.strip('\r').split(',') for i in rawData]
    if parsedData[0] != ["Ticket", "ID", "LAST", "MI", "FIRST", "GR", "Payment Method", "Guest YN", "Guest Ticket "
                                                                                                    "Number"]:
        flash("Invalid CSV", "danger")
        return render_template("upload.html", form=form)

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
    return render_template("upload.html", form=form)


@login_required
def attendees():
    students = Student.query.all()
    guests = Guest.query.all()
    return render_template("attendees.html", students=students, guests=guests)
