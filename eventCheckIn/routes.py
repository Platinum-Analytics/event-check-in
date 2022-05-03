from flask import Blueprint

from . import controllers

main = Blueprint("main", __name__)
action = Blueprint("action", __name__, url_prefix="/action")
password = Blueprint("password", __name__, url_prefix="/password")
verify = Blueprint("email", __name__, url_prefix="/email")

main.add_url_rule("/", "index", controllers.index)
main.add_url_rule("/login", "login", controllers.login, methods=["GET", "POST"])
main.add_url_rule("/upload", "upload", controllers.upload, methods=["GET", "POST"])
main.add_url_rule("/register", "register", controllers.register, methods=["GET", "POST"])
main.add_url_rule("/attendees", "attendees", controllers.attendees)
main.add_url_rule("/home", "home", controllers.home)
main.add_url_rule("/settings", "settings", controllers.settings, methods=["GET", "POST"])
main.add_url_rule("/search", "search", controllers.search, methods=["GET", "POST"])

action.add_url_rule("/logout", "logout", controllers.logout)
action.add_url_rule("/resetDB", "resetDB", controllers.resetDB)
action.add_url_rule("/logStudent/<id_>", "logStudent", controllers.logStudent)
action.add_url_rule("/logGuest/<id_>", "logGuest", controllers.logGuest)

password.add_url_rule("/reauthenticate", "reauthenticate", controllers.reauthenticate, methods=["GET", "POST"])
password.add_url_rule("/forgotPass", "forgotPass", controllers.forgotPass, methods=["GET", "POST"])
password.add_url_rule("/resetPass/<token>", "resetPass", controllers.resetPass, methods=["GET", "POST"])

verify.add_url_rule("/<token>", "email", controllers.email)
