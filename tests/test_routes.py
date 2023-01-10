import pytest
from .fixtures import _app

def test_login_route(_app):
    with _app.test_client() as test:
        response = test.get("/login")
        assert response.status_code == 200

def test_index(_app):
    with _app.test_client() as test:
        response = test.get("/")
        assert response.status_code == 200
