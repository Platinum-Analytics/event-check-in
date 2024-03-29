import os
from datetime import timedelta


class Config(object):
    SECRET_KEY = "fefefefef"

    # flask-login
    USE_SESSION_FOR_NEXT = True
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    # flask-session
    SESSION_TYPE = "sqlalchemy"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)

    # flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "EventCheckIn.Confirmation@gmail.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "Event Check In"
    MAIL_MAX_EMAILS = 5
