from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class csvUpload(FlaskForm):
    csvData = FileField("data", validators=[FileRequired(), FileAllowed(['csv'], "Please Select a csv file!")])
