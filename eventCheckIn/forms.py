from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import EmailField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length


class CSVUpload(FlaskForm):
    csvData = FileField("data", validators=[FileRequired(), FileAllowed(['csv'])])


class UserLogin(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember Me")


class UserRegister(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    confirmPassword = PasswordField("Confirm Password", validators=[InputRequired(), Length(min=8, max=80)])


class ChangePassword(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    currentPassword = PasswordField("Current User Password", validators=[InputRequired()])
    newPassword = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])


class AuthenticateUser(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired()])

