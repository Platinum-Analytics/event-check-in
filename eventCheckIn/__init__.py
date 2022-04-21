from flask import Flask

from .extensions import csrf, db, lm, bc, session
from .routes import *


def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder="ui/templates", static_folder="ui/static")
    app.config.from_object("config.Config")

    # Initialize extensions
    csrf.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    bc.init_app(app)
    session.init_app(app)

    lm.login_view = 'main.login'
    lm.login_message = "Please Log In!"
    lm.login_message_category = "info"

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
