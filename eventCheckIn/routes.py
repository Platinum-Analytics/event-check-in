from flask import Blueprint

from . import actionControllers, mainControllers, passwordControllers, verifyControllers

mainBP = Blueprint("main", __name__)
actionBP = Blueprint("action", __name__, url_prefix="/action")
passwordBP = Blueprint("password", __name__, url_prefix="/password")
verifyBP = Blueprint("email", __name__, url_prefix="/email")

mainBP.add_url_rule("/", "index", mainControllers.index)
mainBP.add_url_rule("/login", "login", mainControllers.login, methods=["GET", "POST"])
mainBP.add_url_rule("/upload", "upload", mainControllers.upload, methods=["GET", "POST"])
mainBP.add_url_rule("/register", "register", mainControllers.register, methods=["GET", "POST"])
mainBP.add_url_rule("/attendees", "attendees", mainControllers.attendees)
mainBP.add_url_rule("/home", "home", mainControllers.home)
mainBP.add_url_rule("/settings", "settings", mainControllers.settings, methods=["GET", "POST"])
mainBP.add_url_rule("/search", "search", mainControllers.search, methods=["GET", "POST"])
mainBP.add_url_rule("/helpPage", "helpPage", mainControllers.helpPage)

actionBP.add_url_rule("/logout", "logout", actionControllers.logout)
actionBP.add_url_rule("/resetDB", "resetDB", actionControllers.resetDB)
actionBP.add_url_rule("/log/<id_>", "log", actionControllers.log)
actionBP.add_url_rule("/removeLog/<entry_id>", "removeLog", actionControllers.removeLog)
actionBP.add_url_rule("/download/<group>", "download", actionControllers.download)
actionBP.add_url_rule("/deleteUser", "deleteUser", actionControllers.deleteUser)

passwordBP.add_url_rule("/reauthenticate", "reauthenticate", passwordControllers.reauthenticate,
                        methods=["GET", "POST"])
passwordBP.add_url_rule("/forgotPass", "forgotPass", passwordControllers.forgotPass, methods=["GET", "POST"])
passwordBP.add_url_rule("/resetPass/<token>", "resetPass", passwordControllers.resetPass, methods=["GET", "POST"])

verifyBP.add_url_rule("/<token>", "email", verifyControllers.email)
