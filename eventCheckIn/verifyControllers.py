from flask import redirect, url_for, flash
from itsdangerous import BadTimeSignature, SignatureExpired

from .extensions import db, timedSerializer
from .models import User_


def email(token):
    try:
        token_email = timedSerializer.loads(token, salt="emailConfirm", max_age=3600)

        user = User_.query.filter_by(email=token_email.lower()).first()
        user.verified = True
        db.session.commit()

        flash("User successfully registered", "success")
    except SignatureExpired:
        flash("Verification expired, please re-register", "danger")
    except BadTimeSignature:
        ...  # Unauthorized, simply redirect to login page
    finally:
        return redirect(url_for("main.login"))
