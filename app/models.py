from sqlalchemy import Table, MetaData
from sqlalchemy.orm import relationship
from . import db

association_table = Table(
    'association_table',
    db.Model.metadata,
    db.Column('user_id', db.ForeignKey('users.id'), primary_key=True),
    db.Column('stop_id', db.ForeignKey('stops.id'), primary_key=True),
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    favorites = relationship('Stop', secondary=association_table,
                             back_populates='user_list')

    def __repr__(self):
        return "<User '%s'>" % self.username

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
