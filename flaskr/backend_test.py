from flaskr.backend import Backend
from unittest.mock import MagicMock, patch
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import pytest
import io


# # # TODO(Project 1): Write tests for Backend methods.
@pytest.fixture
def name():
    return "name"


@pytest.fixture
def mock_blob():
    mock = MagicMock(spec=storage.Blob)
    mock.download_as_text.return_value = None
    return mock


@pytest.fixture
def mock_bucket(mock_blob):
    mock = MagicMock(spec=storage.Bucket)
    mock.blob.return_value = mock_blob
    return mock


@pytest.fixture
def mock_client(mock_bucket):
    mock = MagicMock(spec=storage.Client)
    mock.bucket.return_value = mock_bucket
    return mock


@patch("flaskr.backend.storage.Client")
def test_get_wiki_page(mock_client, mock_blob, mock_bucket, name):
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.get_blob.return_value = mock_blob

    mock_blob.open.return_value = io.StringIO("blob data")

    backend = Backend(mock_client)
    assert backend.get_wiki_page(name) == "blob data"


"""
def test_get_all_page_names():
    pass


def test_upload():
    pass


def test_sign_up():
    pass


def test_sign_in():
    pass


def test_get_image():
    pass
"""
