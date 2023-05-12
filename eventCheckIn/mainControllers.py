import csv
from datetime import datetime

import pytz
from flask import render_template, redirect, url_for, session, flash, request
from flask_login import login_user, login_required, fresh_login_required, current_user
from flask_mail import Message
from sqlalchemy import or_, desc
from sqlalchemy.exc import IntegrityError

from .extensions import db, bc, timedSerializer, mail
from .forms import CSVUpload, UserLogin, UserRegister, ChangePassword, Search
from .models import Student, Guest, User_, TimeEntryGuest, TimeEntryStudent
from .scripts import checkString, checkInt, checkBool, checkCash


def index():
    if current_user.is_active:
        return redirect(url_for("main.home"))
    return redirect(url_for("main.login"))


def login():
    form = UserLogin()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid email/password", "danger")
        return render_template("main/login.html", form=form)

    user = db.session.query(User_).filter_by(email=form.email.data.lower()).first()

    if not user:
        flash("User does not exist", "info")
        return render_template("main/login.html", form=form)
    elif not user.verified:
        flash("Please confirm your email", "warning")
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
                flash("Invalid input", "warning")
            return render_template("main/search.html", form=form)

    form.query.data = form.query.data.strip()
    session["search"] = form.query.data
    students = []
    guests = []
    try:
        query = int(form.query.data)
        students = Student.query.filter(Student.school_id == query).order_by(
            Student.last_name).all()

    except ValueError:
        query = form.query.data.title()

        students = Student.query.filter(or_(Student.first_name == query, Student.last_name == query)).order_by(
            Student.last_name).all()
        guests = Guest.query.filter(or_(Guest.first_name == query, Guest.last_name == query)).all()

    finally:
        for i in students:
            for j in i.guests:
                guests.append(j)

    guests.sort(key=lambda x: x.last_name)

    return render_template("main/search.html", form=form, students=students, guests=guests,
                           total_results=len(guests) + len(students))


@fresh_login_required
def register():
    form = UserRegister()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid email/password", "danger")
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
    def parse_time(string: str, uid: str, is_guest: bool):
        time, staff = string.split("|")
        ltr = "Y" if is_guest else "N"

        timeF = pytz.timezone("America/New_York").localize(datetime.strptime(time, "%b-%d-%Y %I:%M:%S %p")).astimezone(
            pytz.utc)
        return timeF, [staff, uid, ltr]

    form = CSVUpload()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid File Type", "danger")
        return render_template("main/upload.html", form=form)

    # Read and parse CSV Data
    rawData = form.csvData.data.read().decode().split('\n')
    cleanData = []
    for row in rawData:
        if row:
            rowList = row.split("\"")
            if len(rowList) > 1:
                rowList[1] = rowList[1].replace(",", ";")
            cleanData.append("".join(rowList))
    print(cleanData)
    parsedData = [i.strip('\r').split(',') for i in cleanData if i]

    has_log = False
    if parsedData[0] == ["Student #", "Student Name", "# Tickets"]:
        ...
    elif parsedData[0] == ["Student #", "Student Name", "# Tickets", "Check In", "Check Out"]:
        has_log = True
    else:
        flash("Invalid CSV", "danger")
        return render_template("main/upload.html", form=form)

    del parsedData[0]

    # Clear the Student and Guest tables
    db.session.execute(TimeEntryGuest.__table__.delete())
    db.session.execute(TimeEntryStudent.__table__.delete())
    db.session.execute(Guest.__table__.delete())
    db.session.execute(Student.__table__.delete())
    db.session.commit()

    # Store the attendees in the database
    guest_ids = {}
    guests = []
    checkInData = {}
    checkOutData = {}

    for user in parsedData:
        if has_log:
            for i in user[3].split(";"):
                if i:
                    time, info = parse_time(i, user[0], False)
                    checkInData[time] = info
            for i in user[4].split(";"):
                if i:
                    time, info = parse_time(i, user[0], False)
                    checkOutData[time] = info

        print(user[1])
        fName, lName = user[1].split(" ")
        student = Student(checkInt(user[0]), checkString(fName), checkString(lName), False)
        guest = None
        if checkInt(user[2]) > 1:
            student.has_guest = True
            guest = Guest(checkInt(user[0]), "G/O " + checkString(fName), checkString(lName))

        db.session.add(student)
        db.session.add(guest) if guest is not None else ...

    db.session.commit()

    all_attendees = []
    for timeData, info in checkInData.items():
        if info[1] not in all_attendees:
            all_attendees.append(info)

        if info[2] == "N":
            id_ = db.session.query(Student).filter_by(school_id=int(info[1])).first().id
            db.session.add(TimeEntryStudent(True, id_, info[0], timeData))
        else:
            id_ = db.session.query(Guest).filter_by(ticket_num=int(info[1])).first().id
            db.session.add(TimeEntryGuest(True, id_, info[0], timeData))

    for timeData, info in checkOutData.items():
        if info[1] not in all_attendees:
            all_attendees.append(info)

        if info[2] == "N":
            id_ = db.session.query(Student).filter_by(school_id=int(info[1])).first().id
            db.session.add(TimeEntryStudent(False, id_, info[0], timeData))
        else:
            id_ = db.session.query(Guest).filter_by(ticket_num=int(info[1])).first().id
            db.session.add(TimeEntryGuest(False, id_, info[0], timeData))

    db.session.commit()

    for info in all_attendees:
        if info[2] == "N":
            student = db.session.query(Student).filter_by(school_id=int(info[1])).first()
            if student.timeEntries[0].is_check_in:
                student.checked_in = True
        else:
            guest = db.session.query(Guest).filter_by(ticket_num=int(info[1])).first()
            if guest.timeEntries[0].is_check_in:
                guest.checked_in = True

    db.session.commit()
    flash("File Successfully Uploaded!", "success")
    return render_template("main/upload.html", form=form)


@login_required
def attendees():
    stu_filters = {"first_name": Student.first_name, "last_name": Student.last_name, "school_id": Student.school_id}
    guest_filters = {"first_name": Guest.first_name, "last_name": Guest.last_name}

    page = request.args.get("page", 1)
    order = request.args.get("filter", "last_name")
    is_desc = request.args.get("desc") == "True"
    guests = request.args.get("guests") == "True"

    if guests:
        order = guest_filters.get(order, Student.last_name)
    else:
        order = stu_filters.get(order, Student.last_name)

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
                           guests=guests, total_results=len(group))


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
    return render_template("main/help.html")


@login_required
def activityLog():
    student_log = db.session.query(TimeEntryStudent).all()
    guest_log = db.session.query(TimeEntryGuest).all()

    data = [
        [i.student.school_id, i.student.last_name, i.student.first_name,
         "Check In" if i.is_check_in else "Check Out",
         pytz.timezone("UTC").localize(i.time).astimezone(pytz.timezone("America/New_York")).strftime("%r"), i.staff.split("@")[0]] for i in
        student_log]
    temp_data = [
        ["", i.guest.last_name, i.guest.first_name, "Check In" if i.is_check_in else "Check Out",
         pytz.timezone("UTC").localize(i.time).astimezone(pytz.timezone("America/New_York")).strftime("%r"), i.staff.split("@")[0]] for i in guest_log]


    data.extend(temp_data)
    data.sort(key=lambda e: e[5], reverse=True)

    return render_template("main/activityLog.html", data=data)
