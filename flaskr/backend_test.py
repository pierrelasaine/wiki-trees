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


@pytest.fixture
def mock_page_bucket():
    mock = MagicMock(spec=storage.Bucket)

    blobs = [MagicMock() for _ in range(3)]
    blobs[0].name = 'Coast Redwood'
    blobs[1].name = 'Not_A_Tree.png'
    blobs[2].name = 'Japanese Magnolia'

    mock.list_blobs.return_value = blobs
    return mock

@pytest.fixture
def mock_image_bucket():
    mock = MagicMock(spec=storage.Bucket)

    mock.get_blob.return_value = mock_blob
    return mock

@pytest.fixture
def mock_page_storage_client(mock_page_bucket):
    mock = MagicMock(spec=storage.Client)
    mock.bucket.return_value = mock_page_bucket
    return mock

@pytest.fixture
def mock_page_backend(mock_page_storage_client):
    return Backend(mock_page_storage_client)

# Test functions
def test_get_wiki_page(mock_backend):
    """Tests if the get_wiki_page method returns the correct content."""
    assert mock_backend.get_wiki_page(name) == "blob data"


def test_cant_get_wiki_page(mock_backend, bad_name):
    """Tests if the get_wiki_page method returns None for an invalid name."""
    assert mock_backend.get_wiki_page(bad_name) == None


def test_valid_html(mock_backend):
    """Tests if the is_valid_html method returns True for valid HTML."""
    valid_html = '<div><p>Hello, world!</p><a href="https://example.com">Visit example.com</a></div>'
    assert mock_backend.is_valid_html(valid_html)


def test_invalid_doctype(mock_backend):
    """Tests if the is_valid_html method returns False for invalid doctype."""
    invalid_doctype = '<!DOCTYPE other><html><head></head><body></body></html>'
    assert not mock_backend.is_valid_html(invalid_doctype)


def test_unsanitized_html(mock_backend):
    """Tests if the is_valid_html method returns False for unsanitized HTML."""
    unsanitized_html = '<div><p>Hello, world!</p><a href="javascript:alert(1);">Click me</a></div>'
    assert not mock_backend.is_valid_html(unsanitized_html)


def test_missing_closing_tag(mock_backend):
    """Tests if the is_valid_html method returns False for missing closing tag."""
    missing_closing_tag = '<div><p>Hello, world!</p><a href="https://example.com">Visit example.com</div>'
    assert not mock_backend.is_valid_html(missing_closing_tag)


@patch("flaskr.backend.Cleaner")
def test_cleaner_mock(mock_cleaner, mock_backend):
    """
    Tests if the Cleaner class is called with the correct arguments when using the
    is_valid_html method.
    """
    mock_cleaner.return_value = MagicMock(spec=Cleaner)
    valid_html = '<div><p>Hello, world!</p><a href="https://example.com">Visit example.com</a></div>'

    mock_backend.is_valid_html(valid_html)

    mock_cleaner.assert_called_with(tags=[
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code', 'title', 'div',
        'em', 'i', 'li', 'ol', 'p', 'strong', 'u', 'ul', 'img'
    ],
                                    attributes={
                                        'a': ['href', 'title'],
                                        'abbr': ['title'],
                                        'acronym': ['title'],
                                        'img': ['src', 'alt']
                                    })


def test_get_all_page_names(mock_page_backend):
    assert mock_page_backend.get_all_page_names() == ['Coast Redwood', 'Japanese Magnolia']

"""
def test_get_image_with_blob():
    pass

def test_get_image_without_blob():
    

def test_upload(self, username, password, file):
    pass


def test_sign_up(self, username, password):
    pass


def test_sign_in(self, username, password):
    pass
"""

