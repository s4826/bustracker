from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

from log_config import get_logger

logger = get_logger('debug')

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()

from .views import app_bp
from app.login.views import login_bp

login_manager = LoginManager()
login_manager.login_view = 'login_bp.login'

from .models import User
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id = int(user_id)).first()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(app_bp)
    app.register_blueprint(login_bp)

    return app
