from flask import Flask

from .extensions import csrf, db, lm, bc, session, mail
from .routes import mainBP, actionBP, passwordBP, verifyBP


def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder="ui/templates", static_folder="ui/static")
    app.config.from_object("config.Config")

    # Initialize extensions
    csrf.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    bc.init_app(app)
    mail.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db  # Requires db to be initialized
    session.init_app(app)  # Requires SESSION_SQLALCHEMY to be set

    # flask-login defaults
    lm.login_view = 'main.login'
    lm.login_message = "Please Log In"
    lm.login_message_category = "info"

    lm.refresh_view = "password.reauthenticate"
    lm.needs_refresh_message = "Please confirm your password"
    lm.needs_refresh_message_category = "info"

    # Blueprint registration
    app.register_blueprint(mainBP)
    app.register_blueprint(actionBP)
    app.register_blueprint(passwordBP)
    app.register_blueprint(verifyBP)

    with app.app_context():
        db.create_all()

    return app

