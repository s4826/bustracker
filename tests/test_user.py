import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User


def test_password_creation():
    user = User(email='user@test.com', password='password')
    assert not user.verify_password('pass')
    assert user.verify_password('password')

def test_password_access():
    user = User(email='user@test.com', password='password')
    with pytest.raises(AttributeError):
        user.password

