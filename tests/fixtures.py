import pytest
from app import create_app, db

@pytest.fixture
def _app(scope='session'):
    return create_app('testing')

@pytest.fixture
def _db(_app):
    with _app.app_context():
        db.drop_all()
        db.create_all()
