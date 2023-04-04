from flaskr.backend import Backend
<<<<<<< HEAD
from unittest.mock import MagicMock, Mock, patch
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import pytest

=======
from google.cloud import storage
from unittest.mock import patch, MagicMock
import pytest
>>>>>>> 1998949c6cfce2b039a7d8b448fd8facf837b83f
# # # TODO(Project 1): Write tests for Backend methods.
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

<<<<<<< HEAD
def test_get_image(self, image_name):
    pass
=======
# def test_get_image(self, image_name):
#     pass

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
>>>>>>> 1998949c6cfce2b039a7d8b448fd8facf837b83f
