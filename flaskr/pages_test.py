from flaskr import create_app
from unittest.mock import patch, Mock
from google.cloud.storage.blob import Blob
import pytest

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

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to WikiTrees" in resp.data

# TODO(Project 1): Write tests for other routes.
def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"About this Wiki" in resp.data

def test_pages_page(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Wiki Pages" in resp.data

def test_pages_wiki_nonexistent(client):
    resp = client.get("/pages/nonexistent")
    assert resp.status_code == 404
    assert b"Not Found" in resp.data

@patch("google.cloud.storage.bucket.Bucket.get_blob")
def test_pages_wiki_details(mock_get_blob, client):
    mock_blob = Mock(spec=Blob)
    mock_blob.download_as_string.return_value = b"Mock Text for Unit Test\nBiology\nHistory\nFun Fact"
    mock_get_blob.return_value = mock_blob

    resp = client.get("/pages/mock-blob")
    assert resp.status_code == 200
    print(resp.data)
    assert b"Mock Text for Unit Test" in resp.data