from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class CSVUpload(FlaskForm):
    csvData = FileField("data", validators=[FileRequired(), FileAllowed(['csv'])])


class UserLogin(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class UserRegister(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    currentPassword = PasswordField("Current User Password", validators=[InputRequired()])
