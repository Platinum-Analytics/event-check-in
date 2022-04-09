import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")  # same key will be used for csrf protection

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")  # sqlite
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
