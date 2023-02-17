"""Database models for User and Stop"""

from flask import current_app
from flask_login import UserMixin
from flask_mailing import Message
from itsdangerous import TimedSerializer
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager, mail
from .scripts.utils import generate_confirmation_email_content


@login_manager.user_loader
def load_user(user_id):
    """Default user loader for Flask-Login"""
    return db.session.query(User).filter_by(id=int(user_id)).first()


association_table = Table(
    "association_table",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("stop_id", db.ForeignKey("stops.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    """User model, with associated email and password methods"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    pw_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    favorites = relationship(
        "Stop", secondary=association_table, back_populates="user_list"
    )

    @property
    def password(self):
        """Password property"""
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Password setter"""
        self.pw_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify password"""
        return check_password_hash(self.pw_hash, password)

    def create_confirmation_token(self, serializer=None):
        """
        Create a confirmation token for this user.

        :param serializer: Specify an optional serializer for token creation.
        """
        if serializer is None:
            serializer = TimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps(self.id)

    async def send_confirmation_email(self):
        """Send an account confirmation email to this user."""
        token = self.create_confirmation_token()
        message = Message(
            subject="Bustracker Email Address Confirmation",
            recipients=[self.email],
            body=generate_confirmation_email_content(token),
        )
        await mail.send_message(message)

    def __repr__(self):
        return f"<User '{self.email}'>"


class Stop(db.Model):
    """An MBTA stop"""

    __tablename__ = "stops"
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(64))
    last_modified = db.Column(db.DateTime)
    user_list = relationship(
        "User", secondary=association_table, back_populates="favorites"
    )

    def __repr__(self):
        return f"<Stop '{self.id}'>"
