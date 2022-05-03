from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import EmailField, PasswordField, BooleanField, StringField
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
    currentPassword = PasswordField("Current Password", validators=[InputRequired()])
    newPassword = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=80)])
    confirmNewPassword = PasswordField("Confirm New Password", validators=[InputRequired(), Length(min=8, max=80)])


class ForgotPassword(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])


class ResetPassword(FlaskForm):
    newPassword = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=80)])
    confirmNewPassword = PasswordField("Confirm New Password", validators=[InputRequired(), Length(min=8, max=80)])


class ConfirmPassword(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired()])


class Search(FlaskForm):
    query = StringField("Find User", validators=[InputRequired()])
