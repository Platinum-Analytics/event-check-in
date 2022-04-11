from flask import render_template, redirect, url_for, session
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
        return render_template("login.html", form=form, success=False)

    user = User_.query.filter_by(username=form.username.data).first()

    if user and bc.check_password_hash(user.password, form.password.data):
        login_user(user)

        if "next" in session:
            nextVal = session["next"]

            return redirect(nextVal)
    else:
        return render_template("login.html", form=form, success=False)

    return render_template("login.html", form=form, success=True)


@login_required
def register():
    form = UserRegister()
    if not form.validate_on_submit():
        return render_template("register.html", form=form)

    if not bc.check_password_hash(current_user.password, form.currentPassword.data):
        return render_template("register.html", form=form)

    newUser = User_(form.username.data, form.password.data)

    try:
        db.session.add(newUser)
    except IntegrityError:
        db.session.rollback()
        return render_template("register.html", form=form)

    db.session.commit()

    return redirect(url_for("main.login"))


@login_required
def logout():
    logout_user()
    return "<h1>You have been logged out<h1>"


@login_required
def upload():
    form = CSVUpload()
    if not form.validate_on_submit():
        return render_template("upload.html", form=form, success=False)

    # Read and parse CSV Data
    rawData = form.csvData.data.read().decode().split('\n')

    parsedData = [i.strip('\r').split(',') for i in rawData]
    del parsedData[0]

    # Clear the database
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    # Store Students and Guests in database
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
    return render_template("upload.html", form=form, success=True)
