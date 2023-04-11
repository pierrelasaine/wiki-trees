from unittest.mock import patch, MagicMock
from flaskr.backend import Backend
from google.cloud import storage
from bleach import Cleaner
import pytest


# # # TODO(Project 1): Write tests for Backend methods.
"""
def test_get_wiki_page(self, name):
    pass

def test_get_all_page_names(self):
    pass

def test_upload(self, username, password,file):
    pass

def test_sign_up(self, username, password):
    pass

def test_sign_in(self, username, password):
    pass

# def test_get_image(self, image_name):
#     pass
"""


@pytest.fixture
def name():
    return "name"


@pytest.fixture
def bad_name():
    return "bad"


@pytest.fixture
def mock_blob():
    mock = MagicMock(spec=storage.Blob)
    mock.download_as_text.return_value = "blob data"
    return mock


@pytest.fixture
def mock_bucket(mock_blob, bad_name):
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
    mock = MagicMock(spec=storage.Client)
    mock.bucket.return_value = mock_bucket
    return mock


@pytest.fixture
def mock_backend(storage_client):
    return Backend(storage_client)


def test_get_wiki_page(mock_backend):
    assert mock_backend.get_wiki_page(name) == "blob data"


def test_cant_get_wiki_page(mock_backend, bad_name):
    assert mock_backend.get_wiki_page(bad_name) == None


def test_valid_html(mock_backend):
    valid_html = '<div><p>Hello, world!</p><a href="https://example.com">Visit example.com</a></div>'
    assert mock_backend.is_valid_html(valid_html)


def test_invalid_doctype(mock_backend):
    invalid_doctype = '<!DOCTYPE other><html><head></head><body></body></html>'
    assert not mock_backend.is_valid_html(invalid_doctype)


def test_unsanitized_html(mock_backend):
    unsanitized_html = '<div><p>Hello, world!</p><a href="javascript:alert(1);">Click me</a></div>'
    assert not mock_backend.is_valid_html(unsanitized_html)


def test_missing_closing_tag(mock_backend):
    missing_closing_tag = '<div><p>Hello, world!</p><a href="https://example.com">Visit example.com</div>'
    assert not mock_backend.is_valid_html(missing_closing_tag)


@patch("flaskr.backend.Cleaner")
def test_cleaner_mock(mock_cleaner, mock_backend):
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

def test_is_valid_html(mock_backend):
    valid_html = '<div><p>Hello, world!</p><a href="https://example.com">Visit example.com</a></div>'
    assert mock_backend.is_valid_html(valid_html)

def test_invalid_type(mock_backend):
    invalid_doctype = '<!DOCTYPE other><html><head></head><body></body></html>'
    assert not mock_backend.is_valid_html(invalid_doctype)
