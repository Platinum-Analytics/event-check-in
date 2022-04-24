import os
from datetime import timedelta


class Config(object):
    SECRET_KEY = os.urandom(32)

    # flask-login
    USE_SESSION_FOR_NEXT = True
    REMEMBER_COOKIE_DURATION = timedelta(hours=168)

    # flask-session
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # sqlite
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "SMCS2024.PlatinumAnalytics@gmail.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "Platinum Analytics"
    MAIL_MAX_EMAILS = 5

