import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from app import create_app, db
from app.models import User, Stop

@pytest.fixture
def _app(scope='module'):
    return create_app('testing')

@pytest.fixture
def _db(_app):
    with _app.app_context():
        db.drop_all()
        db.create_all()

@pytest.fixture
def user():
    return User(username='test_user')

@pytest.fixture
def stop():
    return Stop(id=2310,
                route_id='77-outbound',
                name='Mass ave opp Waterhouse',
                last_modified=datetime.today())


def test_add_user(_app, _db, user):

    with _app.app_context():
        db.session.add(user)
        db.session.commit()

        user_one = db.session.query(User).first()
        assert user_one.username == 'test_user'
        assert isinstance(user_one.id, int)


def test_add_stop(_app, _db, stop):

    with _app.app_context():
        db.session.add(stop)
        db.session.commit()

        stop_one = db.session.query(Stop).first()
        assert stop_one.id == 2310
        assert stop_one.route_id == '77-outbound'
        assert stop_one.name == 'Mass ave opp Waterhouse'


def test_user_stop_relationship(_app, _db, user, stop):
    with _app.app_context():
        user.favorites.append(stop)
        db.session.add_all([user, stop])
        db.session.commit()

        u = db.session.query(User).first()
        assert u.favorites[0] == stop
        assert stop.user_list[0] == u
