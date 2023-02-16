"""App factory module"""

# flake8: noqa
from flask import Flask
from config import config
from .extensions import (
    bootstrap,
    db,
    migrate,
    session,
    mail,
    login_manager
)

from .views import app_bp
from .login.views import login_bp

login_manager.login_view = 'login_bp.login'


def create_app(config_name):
    """App factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(app_bp)
    app.register_blueprint(login_bp)

    return app
