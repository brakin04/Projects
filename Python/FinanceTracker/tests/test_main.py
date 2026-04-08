from app.models import User
from werkzeug.security import generate_password_hash
from flask_login import current_user

#------------------------------------------------
def test_get_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to your finance tracker!" in response.data

# dashboard tests
#------------------------------------------------
def test_get_dashboard_unauthenticated(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data
    assert response.request.path == '/login'

def test_get_dashboard_authenticated(client, db_setup):
    user = User(email='taken@test.com', nickname='original', password=generate_password_hash('hash'), security_answers=['a','b','c'])
    db_setup.session.add(user)
    db_setup.session.commit()
    client.post('/login', data={
        'identity': 'taken@test.com',
        'password': 'hash'
    })
    with client.application.test_request_context():
        assert current_user.is_authenticated
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'

# Profile tests
#------------------------------------------------
def test_get_profile_unauthenticated(client):
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data
    assert response.request.path == '/login'

def test_get_profile_authenticated(client, db_setup):
    user = User(email='email@test.com', nickname='profile', password=generate_password_hash('hash'), security_answers=['a','b','c'])
    db_setup.session.add(user)
    db_setup.session.commit()
    client.post('/login', data={
        'identity': 'email@test.com',
        'password': 'hash'
    })
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/profile'

# logging-info tests
#------------------------------------------------
def test_get_logging_info_unauthenticated(client):
    response = client.get('/logging-info', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data
    assert response.request.path == '/login'

def test_get_logging_info_authenticated(client, db_setup):
    user = User(email='email@test.com', nickname='profile', password=generate_password_hash('hash'), security_answers=['a','b','c'])
    db_setup.session.add(user)
    db_setup.session.commit()
    client.post('/login', data={
        'identity': 'email@test.com',
        'password': 'hash'
    })
    response = client.get('/logging-info', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/logging-info'