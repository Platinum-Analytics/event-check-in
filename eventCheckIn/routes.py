from flask import Blueprint

from . import controllers

main = Blueprint("main", __name__)

main.add_url_rule("/", "index", controllers.index)
main.add_url_rule("/login", "login", controllers.login, methods=['GET', 'POST'])
main.add_url_rule("/upload", "upload", controllers.upload, methods=['GET', 'POST'])
main.add_url_rule("/logout", "logout", controllers.logout)
main.add_url_rule("/register", "register", controllers.register, methods=['GET', 'POST'])
main.add_url_rule("/attendees", "attendees", controllers.attendees)
main.add_url_rule("/home", "home", controllers.home)
