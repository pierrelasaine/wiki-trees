from flaskr import create_app
from unittest.mock import patch, MagicMock
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
    assert b"home-box" in resp.data


def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"About Us!" in resp.data


@patch("flaskr.backend.Backend.get_image")
def test_get_image(mock_get_image, client):
    mock_get_image.return_value = os.urandom(1024)

    resp = client.get("/images/mock_image")
    assert resp.status_code == 200


def test_image_nonexistent(client):
    resp = client.get("/images/nonexistent")
    assert resp.status_code == 404
    assert b"Not Found" in resp.data


# def other_test_pages_page(client):
# resp = client.get("/pages")
# assert resp.status_code == 200
# assert b"Wiki Pages" in resp.data


@patch("flaskr.backend.Backend.get_wiki_page")
def test_pages_wiki_nonexistent(mock_get_wiki_page, client):
    mock_get_wiki_page.return_value = None
    resp = client.get("/pages/nonexistent")
    assert resp.status_code == 404
    assert b"Not Found" in resp.data


@patch("flaskr.backend.Backend.get_wiki_page")
def test_page_details(mock_get_wiki_page, client):
    mock_get_wiki_page.return_value = "<p>Mock Text for Unit Test</p>"

    resp = client.get("/pages/mock-page")
    assert resp.status_code == 200
    assert b"Mock Text for Unit Test" in resp.data


def test_upload_page(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"Drop File to Upload" in resp.data


def test_upload_valid_html(client):
    resp = client.post(
        '/upload',
        data={
            'name': 'valid_page',
            'content': '<html><body><h1>Hello world!</h1></body></html>'
        })
    assert resp.status_code == 302


def no_test_upload_invalid_html(client):
    resp = client.post(
        '/upload',
        data={
            'name': 'invalid_page',
            'content': '<html><body><h1>Hello world!</h2></body></html>'
        })
    assert resp.status_code == 200
    assert b"Invalid HTML!" in resp.data


@patch("flaskr.backend.Backend.get_wiki_page")
@patch("flaskr.backend.Backend.upload")
def test_TinyMCE_upload(mock_upload, mock_get_wiki_page, client):
    mock_upload.return_value = None
    mock_get_wiki_page.return_value = "Test HTML"
    resp = client.post("/upload",
                       data=dict(name="test_page", content="<p>Test HTML</p>"))
    assert resp.status_code == 302
    resp = client.get("/pages/test_page")
    assert resp.status_code == 200
    assert b"Test HTML" in resp.data


"""
@patch("flaskr.backend.Backend.get_wiki_page")
@patch("flaskr.backend.Backend.upload")
def test_file_upload(mock_upload, mock_get_wiki_page, client):
    mock_upload.return_value = None
    mock_get_wiki_page.return_value = "Test HTML"
    resp = client.post("/upload",
                        data=dict(name="test_page",
                                  fileb=FileStorage(filename="test.html", stream=b"<p>Test HTML</p>")))
    resp = client.get("/pages/test_page")
    assert resp.status_code == 200
    assert b"Test HTML" in resp.data
"""


def pytest_configure(config):
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
