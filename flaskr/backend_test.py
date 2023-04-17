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
def storage_client(mock_bucket):
    """Returns a MagicMock object with the same spec as storage.Client."""
    mock = MagicMock(spec=storage.Client)
    mock.bucket.return_value = mock_bucket
    return mock

@pytest.fixture
def mock_blob():
    """
    Returns a MagicMock object with the same spec as storage.Blob,
    configured to return "blob data" when download_as_text is called.
    """
    mock = MagicMock(spec=storage.Blob)
    mock.download_as_text.return_value = "blob data"
    
    return mock

@pytest.fixture
def mock_bucket(mock_blob, bad_name):
    """
    Returns a MagicMock object with the same spec as storage.Bucket.
    Configured to return the correct mock_blob based on the provided name.
    """
    mock = MagicMock(spec=storage.Bucket)

    def side_effect(name):
        if name == bad_name:
            bad_mock = MagicMock(spec=storage.Blob)
            bad_mock.download_as_text.return_value = None
            return bad_mock
        else:
            return mock_blob

    mock.blob.side_effect = side_effect
    return mock



@pytest.fixture
def mock_backend(storage_client):
    """Returns a Backend instance configured to use the provided storage_client."""
    mock = MagicMock()
    mock.page_bucket.list_blobs.return_value = ["Coast Redwood", "Gingko", "Juniper"]
    return mock(storage_client)

# Test functions
def test_get_wiki_page(mock_backend):
    """Tests if the get_wiki_page method returns the correct content."""
    assert mock_backend.get_wiki_page(name) == "blob data"


def test_cant_get_wiki_page(mock_backend, bad_name):
    """Tests if the get_wiki_page method returns None for an invalid name."""
    assert mock_backend.get_wiki_page(bad_name) == None


def test_get_all_page_names(mock_backend):
    assert mock_backend.get_all_page_names() == ["Coast Redwood", "Gingko", "Juniper"]

def test_upload():
    pass

def test_sign_up():
    pass

def test_sign_in():
    pass

def test_get_image():
    pass
