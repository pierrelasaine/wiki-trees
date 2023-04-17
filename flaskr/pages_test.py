from flaskr import create_app
from unittest.mock import patch
from werkzeug.datastructures import FileStorage
from flaskr.pages import *
import io
import pytest
import os
import warnings


@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SECRET_KEY': 'test'})
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_serve_js(client):
    resp = client.get("/src/main.js")

    assert resp.status_code == 200


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
    assert b'Sorry! The page could not be found :(' in resp.data


@patch("flaskr.backend.Backend.get_wiki_page")
def test_pages_wiki_nonexistent(mock_get_wiki_page, client):
    mock_get_wiki_page.return_value = None

    resp = client.get("/pages/nonexistent")

    assert resp.status_code == 404
    assert b"Sorry! The page could not be found :(" in resp.data


@patch("flaskr.backend.Backend.get_wiki_page")
def test_page_details(mock_get_wiki_page, client):
    mock_get_wiki_page.return_value = "<p>Mock Text for Unit Test</p>"

    resp = client.get("/pages/mock-page")

    assert resp.status_code == 200
    assert b"Mock Text for Unit Test" in resp.data


def test_upload_page(client):
    resp = client.get("/upload")

    assert resp.status_code == 200
    assert b"Upload!" in resp.data


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


@patch("flaskr.backend.Backend.get_wiki_page")
@patch("flaskr.backend.Backend.upload")
def test_file_upload(mock_upload, mock_get_wiki_page, client):
    mock_upload.return_value = None
    mock_get_wiki_page.return_value = "Test HTML"

    resp = client.post("/upload",
                       data=dict(name="test_page",
                                 file=FileStorage(filename="test.html",
                                                  stream=b"<p>Test HTML</p>")))

    #assert resp.status_code == 302

    resp = client.get("/pages/test_page")

    assert resp.status_code == 200
    assert b"Test HTML" in resp.data


def pytest_configure(config):
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
