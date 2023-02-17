from datetime import datetime

import pytest
from app import db
from app.models import Stop, User


@pytest.fixture
def stop():
    return Stop(
        id=2310,
        route_id="77-outbound",
        name="Mass ave opp Waterhouse",
        last_modified=datetime.today(),
    )


def test_add_user(_app, _db, user):
    with _app.app_context():
        db.session.add(user)
        db.session.commit()

        user_one = db.session.query(User).first()
        assert user_one.email == "user@test.com"
        assert isinstance(user_one.id, int)


def test_add_stop(_app, _db, stop):
    with _app.app_context():
        db.session.add(stop)
        db.session.commit()

        stop_one = db.session.query(Stop).first()
        assert stop_one.id == 2310
        assert stop_one.route_id == "77-outbound"
        assert stop_one.name == "Mass ave opp Waterhouse"


def test_user_stop_relationship(_app, _db, user, stop):
    with _app.app_context():
        user.favorites.append(stop)
        db.session.add_all([user, stop])
        db.session.commit()

        u = db.session.query(User).first()
        assert u.favorites[0] == stop
        assert stop.user_list[0] == u
