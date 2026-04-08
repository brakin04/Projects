import pytest
import logging
from app import create_app, db

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-key'
    FILE_HANDLER = logging.FileHandler('log_file_path')
    FILE_HANDLER.setLevel(logging.DEBUG)

@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app

@pytest.fixture
def client(app):
    # This provides the 'client' argument to your tests
    return app.test_client()

@pytest.fixture
def db_setup(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

# run using: python3 -m pytest
# see which p/f: python3 -m pytest -v
# specific file: python3 -m pytest tests/test_auth.py