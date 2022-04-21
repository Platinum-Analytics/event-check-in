import os
from datetime import timedelta


class Config(object):
    SECRET_KEY = os.urandom(32)
    USE_SESSION_FOR_NEXT = True

    REMEMBER_COOKIE_DURATION = timedelta(hours=168)

    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # sqlite
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
