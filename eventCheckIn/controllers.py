from flask import request, render_template, redirect, url_for
from .models import *
from .forms import csvUpload


def index():
    return redirect(url_for("main.login"))


def login():
    return "<h1>My Login Page</h1>"


def upload():
    form = csvUpload()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("Worked")
        return render_template("upload.html", success=True)

    return render_template("upload.html", form=form, success=False)
