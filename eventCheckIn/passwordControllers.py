from flask import render_template, redirect, url_for, session, flash
from flask_login import login_required, confirm_login, current_user
from flask_mail import Message
from itsdangerous import BadTimeSignature, SignatureExpired

from .extensions import db, bc, timedSerializer, mail
from .forms import ConfirmPassword, ForgotPassword, ResetPassword
from .models import User_


@login_required
def reauthenticate():
    form = ConfirmPassword()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid password", "warn")
        return render_template("password/reauthenticate.html", form=form)

    if not bc.check_password_hash(current_user.password, form.password.data):
        flash("Incorrect password", "danger")
        return render_template("password/reauthenticate.html", form=form)

    confirm_login()
    flash("Password confirmed", "success")

    if "next" in session:
        next_val = session["next"]
        if next_val.split("/")[1] != "action":
            return redirect(next_val)

    return render_template("main/home.html")


def forgotPass():
    form = ForgotPassword()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Invalid Email", "warn")
        return render_template("password/forgotPass.html", form=form)

    user = db.session.query(User_).filter_by(email=form.email.data.lower()).first()

    if not user:
        flash("User does not exist", "info")
        return render_template("password/forgotPass.html", form=form)
    elif not user.verified:
        flash("User not verified;  Please re-register", "warn")

    reset_email = Message("Event Check In Password Reset",
                          sender="Event Check In",
                          recipients=[form.email.data])

    reset_email.html = render_template("email/resetEmail.html",
                                       token=timedSerializer.dumps(form.email.data,
                                                                   salt="resetPass"))

    mail.send(reset_email)

    flash("Password reset form sent, please check your email", "success")
    return redirect(url_for("main.login"))


def resetPass(token):
    try:
        token_email = timedSerializer.loads(token, salt="resetPass", max_age=3600)
    except SignatureExpired:
        flash("Verification expired, please re-register", "danger")
        return redirect(url_for("main.login"))
    except BadTimeSignature:
        return redirect(url_for("main.login"))  # Unauthorized, simply redirect to login page

    form = ResetPassword()
    if not form.validate_on_submit():
        if len(form.errors) != 0:
            flash("Error", "danger")
        return render_template("password/resetPass.html", form=form, token=token)

    if form.newPassword.data != form.confirmNewPassword.data:
        flash("Passwords do not match", "warn")
        return render_template("password/resetPass.html", form=form, token=token)

    user = db.session.query(User_).filter_by(email=token_email.lower()).first()
    user.changePassword(form.newPassword.data)
    db.session.commit()

    flash("Password successfully reset", "success")
    return redirect(url_for("main.login"))
