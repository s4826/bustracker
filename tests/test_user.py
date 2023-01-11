import pytest
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from .fixtures import _app


def test_password_verification():
    user = User(email='user@test.com', password='password')
    assert not user.verify_password('pass')
    assert user.verify_password('password')

def test_password_access():
    user = User(email='user@test.com', password='password')
    with pytest.raises(AttributeError):
        user.password

def test_user_login(_app):
    user = User(email='user@test.com', password='password')
    with _app.app_context():
        with _app.test_request_context():
            assert not current_user.is_authenticated
            login_user(user)
            assert current_user.is_authenticated

    with _app.test_request_context():
        with _app.test_request_context():
            logout_user()
            assert not current_user.is_authenticated
