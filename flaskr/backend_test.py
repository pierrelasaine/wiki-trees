from flaskr.backend import Backend
from unittest.mock import MagicMock, Mock, patch
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import pytest

# # # TODO(Project 1): Write tests for Backend methods.
def test_get_wiki_page():
    pass

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


@pytest.fixture
def matches():
    return ["apple", "allep", "app", "pear", "pineapple"]

def test_search():
    pass