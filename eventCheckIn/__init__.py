from flask import Flask

from .extensions import csrf, db, lm, bc, session, mail
from .routes import main, verify


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

    lm.login_view = 'main.login'
    lm.login_message = "Please Log In"
    lm.login_message_category = "info"

    lm.refresh_view = "main.reauthenticate"
    lm.needs_refresh_message = "Please confirm your password"
    lm.needs_refresh_message_category = "info"

    app.register_blueprint(main)
    app.register_blueprint(verify)

    with app.app_context():
        db.create_all()

    return app
