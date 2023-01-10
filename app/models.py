from flask_login import UserMixin
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

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
