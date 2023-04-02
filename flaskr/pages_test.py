from flaskr import create_app
from unittest.mock import patch
from werkzeug.datastructures import FileStorage
from flaskr.pages import *
import io
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


def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"About this Wiki" in resp.data


@patch("flaskr.backend.backend2.get_image")
def test_get_image(mock_get_image, client):
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
    mock_get_wiki_page.return_value = "Mock Text for Unit Test\n2\n3\n4"

    resp = client.get("/pages/mock-page")
    assert resp.status_code == 200
    assert b"Mock Text for Unit Test" in resp.data


def test_upload_page(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"Drop File to Upload" in resp.data


@patch("flaskr.backend.backend1.get_wiki_page")
@patch("flaskr.backend.backend1.bucket_upload")
def test_TinyMCE_upload(mock_bucket_upload, mock_get_wiki_page, client):
    mock_bucket_upload.return_value = None
    mock_get_wiki_page.return_value = "Test HTML"
    resp = client.post("/upload",
                       data=dict(name="test_page",
                                 content="<p>Test HTML</p>"))
    assert resp.status_code == 302
    resp = client.get("/pages/test_page")
    assert resp.status_code == 200
    assert b"Test HTML" in resp.data

# ask Bianca about weird syntax req in line 99
"""
@patch("flaskr.backend.backend1.get_wiki_page")
@patch("flaskr.backend.backend1.bucket_upload")
def test_file_upload(mock_bucket_upload, mock_get_wiki_page, client):
    mock_bucket_upload.return_value = None
    mock_get_wiki_page.return_value = "Test HTML"
    resp = client.post("/upload",
                        data=dict(name="test_page",
                             TODO file=FileStorage(filename="test.html", stream=b"<p>Test HTML</p>")
    assert resp.status_code == 302 \
    resp = client.get("/pages/test_page")
    assert resp.status_code == 200
    assert b"Test HTML" in resp.data
"""

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
