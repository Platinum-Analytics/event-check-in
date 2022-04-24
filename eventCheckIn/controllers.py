from flask import render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, fresh_login_required, confirm_login, current_user
from flask_mail import Message
from itsdangerous import BadTimeSignature, SignatureExpired

from .extensions import db, bc, timedSerializer, mail
from .forms import CSVUpload, UserLogin, UserRegister, AuthenticateUser, ChangePassword
from .models import Student, Guest, User_
from .scripts import checkString, checkInt, checkBool, checkCash


def index():
    return redirect(url_for("main.home"))


def login():
    form = UserLogin()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid email/password", "warn")
        return render_template("login.html", form=form)

    user = User_.query.filter_by(email=form.email.data).first()

    if not user:
        flash("User does not exist", "info")
        return render_template("login.html", form=form)
    elif not user.verified:
        flash("Please confirm your email", "warn")
    elif not bc.check_password_hash(user.password, form.password.data):
        flash("Incorrect password!", "danger")
        return render_template("login.html", form=form)

    login_user(user, remember=form.remember.data)
    flash("Logged in successfully!", "success")

    if "next" in session:
        next_val = session["next"]
        if next_val != "/logout":
            return redirect(next_val)

    return redirect(url_for("main.home"))


@login_required
def home():
    return render_template("home.html")


@fresh_login_required
def register():
    form = UserRegister()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid email/password", "warn")
        return render_template("register.html", form=form)

    user_search = User_.query.filter_by(email=form.email.data).first()
    if user_search:
        if user_search.verified:
            flash("Email already registered", "info")
            return render_template("register.html", form=form)
        else:
            db.session.delete(user_search)
            db.session.commit()

    if form.password.data != form.confirmPassword.data:
        flash("Passwords do not match", "danger")
        return render_template("register.html", form=form)

    user = User_(form.email.data, form.password.data, False)
    db.session.add(user)
    db.session.commit()

    confirm_email = Message("Event Check In Email Confirmation",
                            sender=("Platinum Analytics", "SMCS2024.PlatinumAnalytics.com"),
                            recipients=[form.email.data])

    confirm_email.html = render_template("verify/email.html", token=timedSerializer.dumps(form.email.data))
    mail.send(confirm_email)

    flash("Email verification sent, please confirm your email", "success")
    return redirect(url_for("main.login"))


def verify(token):
    try:
        email = timedSerializer.loads(token, max_age=3600)

        user = User_.query.filter_by(email=email).first()
        user.verified = True
        db.session.commit()

        flash("User successfully registered", "success")
    except SignatureExpired:
        flash("Verification expired, please re-register", "danger")
    except BadTimeSignature:
        ...  # Unauthorized, simply redirect to login page
    finally:
        return redirect(url_for("main.login"))


@login_required
def logout():
    logout_user()
    flash("Successfully logged out!", "success")
    return redirect(url_for("main.login"))


@login_required
def upload():
    form = CSVUpload()
    print(form.csvData.data)
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


@fresh_login_required
def settings():
    return render_template("settings.html")


@login_required
def reauthenticate():
    form = AuthenticateUser()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid password", "warn")
        return render_template("reauthenticate.html", form=form)

    if not bc.check_password_hash(current_user.password, form.password.data):
        flash("Incorrect password!", "danger")
        return render_template("reauthenticate.html", form=form)

    confirm_login()
    flash("Password confirmed", "success")

    if "next" in session:
        next_val = session["next"]
        if next_val != "/logout":
            return redirect(next_val)

    return render_template("home.html")
