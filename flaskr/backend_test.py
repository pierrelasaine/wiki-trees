from flaskr.backend import Backend
from unittest.mock import MagicMock, Mock, patch
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import pytest

# # # TODO(Project 1): Write tests for Backend methods.
@pytest.fixture
def name():
    return "name"

@pytest.fixture
def mock_blob():
    return MagicMock(spec=storage.Blob)

@pytest.fixture
def mock_bucket():
    return MagicMock(spec=storage.Bucket)

@patch("flaskr.backend.storage.Client")
def test_get_wiki_page(mock_client, mock_blob, mock_bucket, name):
    mock_client.return_value.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    mock_blob.download_as_text.return_value  = "blob data"

    backend = Backend(name)
    assert backend.get_wiki_page(name) == "blob data"

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
