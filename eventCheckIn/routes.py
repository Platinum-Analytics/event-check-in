from flask import Blueprint
from . import controllers

main = Blueprint("main", __name__)
main.add_url_rule("/", "index", controllers.index)
main.add_url_rule("/login", "login", controllers.login)
