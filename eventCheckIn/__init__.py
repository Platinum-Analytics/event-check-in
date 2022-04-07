from flask import Flask, redirect, url_for, render_template
from .extensions import *

from .routes import *


def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder="ui/templates", static_folder="ui/static")
    app.config.from_pyfile("config_app.py")

    # init extensions
    csrf.init_app(app)
    db.init_app(app)

    # TODO - register blueprints here. e.g.
    app.register_blueprint(main)

    # # finally create tables as per models
    # db.create_all()

    return app
