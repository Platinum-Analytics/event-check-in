import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")  # same key will be used for csrf protection
    USE_SESSION_FOR_NEXT = True

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # sqlite
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
