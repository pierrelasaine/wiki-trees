from flaskr import create_app
from unittest.mock import patch, Mock
from google.cloud.storage.blob import Blob
from flaskr.backend import Backend
from flaskr.pages import *
import pytest
import os

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to WikiTrees" in resp.data

# TODO(Project 1): Write tests for other routes.
def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"About this Wiki" in resp.data

@patch("flaskr.backend.backend2.get_image")
def test_get_image(mock_get_image, client):
    with patch("flaskr.pages.is_valid_blob") as mock_valid_blob:
        mock_valid_blob.return_value = True
        mock_get_image.return_value = os.urandom(1024)

        resp = client.get("/images/mock_image")
        assert resp.status_code == 200

def test_image_nonexistent(client):
    resp = client.get("/images/nonexistent")
    assert resp.status_code == 404
    assert b"Not Found" in resp.data

def test_pages_page(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Wiki Pages" in resp.data

def test_pages_wiki_nonexistent(client):
    resp = client.get("/pages/nonexistent")
    assert resp.status_code == 404
    assert b"Not Found" in resp.data

@patch("flaskr.backend.backend1.get_wiki_page")
def test_page_details(mock_get_wiki_page, client):
    with patch("flaskr.pages.is_valid_blob") as mock_valid_blob:
        mock_valid_blob.return_value = True
        mock_get_wiki_page.return_value = "Mock Text for Unit Test\n2\n3\n4"

        resp = client.get("/pages/mock-page")
        assert resp.status_code == 200
        assert b"Mock Text for Unit Test" in resp.data

def test_new_signup_success(client):
    response = client.post('/signup', data=dict(username='new_user', password='new_password'))
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'


def test_new_signup_username_already_exists(client):
    response = client.post('/signup', data=dict(username='existing_user', password='password'))
    assert response.status_code == 200
    assert b'Username already exists!' in response.data


def test_user_login_success(client):
    response = client.post('/login', data=dict(username='existing_user', password='password'))
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'


def test_user_login_incorrect_password(client):
    response = client.post('/login', data=dict(username='existing_user', password='incorrect_password'))
    assert response.status_code == 200 
    assert b'Invalid username or password' in response.data


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'