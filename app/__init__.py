from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()

from .views import app_bp
from .login import login_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(app_bp)
    app.register_blueprint(login_bp)

    return app
