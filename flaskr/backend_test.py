"""This module contains tests for the Backend class in the flaskr application.
"""
from unittest.mock import patch, MagicMock
from flaskr.backend import Backend
from google.cloud import storage
from bleach import Cleaner
import pytest
import io


# Test fixtures
@pytest.fixture
def name():
    """Returns a string representing a valid name."""
    return "name"


@pytest.fixture
def bad_name():
    """Returns a string representing an invalid name."""
    return "bad"


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
def storage_client(mock_bucket):
    """Returns a MagicMock object with the same spec as storage.Client."""
    mock = MagicMock(spec=storage.Client)
    mock.bucket.return_value = mock_bucket
    return mock


@pytest.fixture
def mock_backend(storage_client):
    """Returns a Backend instance configured to use the provided storage_client."""
    return Backend(storage_client)

# Test Functions

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
