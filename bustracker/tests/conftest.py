import pytest

from bustracker.app import create_app, db
from bustracker.app.models import User


@pytest.fixture(scope="session")
def _app():
    return create_app("testing")


@pytest.fixture
def _db(_app):
    with _app.app_context():
        db.drop_all()
        db.create_all()


@pytest.fixture()
def client(_app):
    return _app.test_client()


@pytest.fixture
def user():
    return User(email="user@test.com", password="password")


@pytest.fixture
def test_mail_server(_app):
    return "http://{}:{}".format(
        _app.config["MAIL_SERVER"], _app.config["MAIL_API_PORT"]
    )
