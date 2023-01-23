"""Flask extensions for app functionality"""

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mailing import Mail
from flask_session import Session

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
session = Session()
mail = Mail()
login_manager = LoginManager()
