from flask import request, render_template, redirect, url_for
from .models import *


def index():
    return redirect(url_for("main.login"))


def login():
    return "<h1>My Login Page</h1>"
