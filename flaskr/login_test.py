from flaskr import create_app
import pytest


@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SECRET_KEY': 'test'})
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_new_signup(client):
    response = client.post('/signup',
                           data=dict(username='test_user',
                                     password='test_password'))
    assert response.status_code == 200


def test_new_signup_existing_user(client):
    response = client.post('/signup',
                           data=dict(username='test_user',
                                     password='test_password'))
    response = client.post('/signup',
                           data=dict(username='test_user',
                                     password='test_password'))
    assert response.status_code == 200
    assert b'Username already exists!' in response.data


def test_user_login_logout(client):
    # log in test
    response = client.post('/signup',
                           data=dict(username='test_user',
                                     password='test_password'))
    response = client.post('/login',
                           data=dict(username='test_user',
                                     password='test_password'))
    assert response.status_code == 302
    # log out test
    response = client.get("/logout")
    assert response.status_code == 302


def test_user_login_incorrect_password(client):
    response = client.post('/signup',
                           data=dict(username='test_user',
                                     password='test_password'))
    response = client.post('/login',
                           data=dict(username='test_user',
                                     password='bad_password'))
    assert response.status_code == 200
    assert b'Incorrect username or password' in response.data
