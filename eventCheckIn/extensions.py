import os

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from itsdangerous import URLSafeSerializer

csrf = CSRFProtect()
db = SQLAlchemy()
lm = LoginManager()
bc = Bcrypt()
session = Session()
serializer = URLSafeSerializer(os.urandom(32))
