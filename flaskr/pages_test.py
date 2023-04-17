from flaskr import create_app
from unittest.mock import patch, Mock
from google.cloud.storage.blob import Blob
from flaskr.backend import Backend
from flaskr.pages import *
import pytest
import os
import warnings


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SECRET_KEY': 'test'})
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to WikiTrees" in resp.data


# # TODO(Project 1): Write tests for other routes.
def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"About this Wiki" in resp.data


@patch("flaskr.backend.backend")
def test_get_image(mock_backend, client):
    with patch("flaskr.pages.is_valid_blob") as mock_valid_blob:
        mock_backend.valid_blob.return_value = True
        mock_backend.get_image.return_value = os.urandom(1024)

        resp = client.get("/images/mock_image")
        assert resp.status_code == 200


def test_image_nonexistent(client):
    resp = client.get("/images/nonexistent")
    assert resp.status_code == 404
    assert b"Not Found" in resp.data

@patch("flaskr.backend")
def test_pages_post(mock_backend, client):
    mock_backend.search.return_value = ["Oak Tree"]
    response = client.post("/pages", data = {"search_input": "Oak Tree"})
    assert response.status_code == 200
    assert b'Oak Tree' in response.data
    assert b'Evergreen' not in response.data



def test_pages_page(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Wiki Pages" in resp.data


def test_pages_wiki_nonexistent(client):
    resp = client.get("/pages/nonexistent")
    assert resp.status_code == 404
    assert b"Not Found" in resp.data


@patch("flaskr.backend")
def test_page_details(mock_backend, client):
    with patch("flaskr.pages.is_valid_blob") as mock_valid_blob:
        mock_backend.valid_blob.return_value = True
        mock_backend.get_wiki_page.return_value = "Mock Text for Unit Test\n2\n3\n4"

        resp = client.get("/pages/mock-page")
        assert resp.status_code == 200
        assert b"Mock Text for Unit Test" in resp.data


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


def test_user_login(client):
    response = client.post('/signup',
                           data=dict(username='test_user',
                                     password='test_password'))
    response = client.post('/login',
                           data=dict(username='test_user',
                                     password='test_password'))
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


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302


def pytest_configure(config):
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
