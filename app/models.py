from flask import current_app
from flask_login import UserMixin
from flask_mailing import Message
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedSerializer

from . import db, mail
from .scripts.utils import generate_confirmation_email_content

association_table = Table(
    'association_table',
    db.Model.metadata,
    db.Column('user_id', db.ForeignKey('users.id'), primary_key=True),
    db.Column('stop_id', db.ForeignKey('stops.id'), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    pw_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    favorites = relationship('Stop', secondary=association_table,
                             back_populates='user_list')

    @property
    def password(self):
        raise AttributeError("Cannot read password")

    @password.setter
    def password(self, password):
        self.pw_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def create_confirmation_token(self, serializer=None):
        if serializer is None:
            serializer = TimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.id)

    async def send_confirmation_email(self):
        token = self.create_confirmation_token()
        message = Message(
                subject='Bustracker Email Address Confirmation',
                recipients=[self.email],
                body=generate_confirmation_email_content(token)
                )
        await mail.send_message(message)

    def __repr__(self):
        return "<User '%s'>" % self.email


class Stop(db.Model):
    __tablename__ = 'stops'
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(64))
    last_modified = db.Column(db.DateTime)
    user_list = relationship("User", secondary=association_table,
                             back_populates='favorites')

    def __repr__(self):
        return "<Stop '%d'>" % self.id
