import os

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_mail import Mail

from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer

csrf = CSRFProtect()
db = SQLAlchemy()
lm = LoginManager()
bc = Bcrypt()
session = Session()
mail = Mail()

serializer = URLSafeSerializer(os.urandom(32))
timedSerializer = URLSafeTimedSerializer(os.urandom(32))
