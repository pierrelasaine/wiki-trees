from unittest.mock import patch, MagicMock
from flaskr.backend import Backend
from google.cloud import storage
from bleach import Cleaner
import pytest
import folium
from folium.plugins import MarkerCluster
from bs4 import BeautifulSoup


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
@pytest.fixture
def valid_html():
    return '<div><p>Hello, world!</p><a href="https://example.com">Visit example.com</a></div>'

@pytest.fixture
def invalid_doctype():
    return '<!DOCTYPE other><html><head></head><body></body></html>'

def test_is_html(mock_backend, valid_html):
    assert mock_backend.is_valid_html(valid_html)

def test_invalid_type(mock_backend, invalid_doctype):
    assert not mock_backend.is_valid_html(invalid_doctype)

def test_legend(mock_backend):
    map_html = mock_backend.tree_map()
    assert 'Legend' in map_html
    assert 'Coast Redwood' in map_html
    # assert 'style="background-color:forestgreen' in map_html

def test_tree_distribution(mock_backend):
    tree_locations = {
        'Coast Redwood': {'location': (38.9822, -123.3781), 'distribution': 'North America'},
        'Ginko': {'location': (39.7684, -86.1581), 'distribution': 'East Asia'},
        'Japanese Magnolia': {'location': (35.8801, -79.0800), 'distribution': 'East Asia'},
        'Juniper': {'location': (40.7968, -77.8619), 'distribution': 'North America, Eurasia'},
        'Live Oak': {'location': (30.3894, -86.5229), 'distribution': 'North America'},
        'Monterey Cypress': {'location': (36.6002, -121.8947), 'distribution': 'North America'},
        'Palm': {'location': (26.7056, -80.0364), 'distribution': 'Africa, Eurasia, Americas'},
        'Palmetto': {'location': (26.7153, -81.0522), 'distribution': 'North America'},
        'Water Oak': {'location': (30.4383, -84.2807), 'distribution': 'North America'},
        'White Oak': {'location': (33.9860, -83.7185), 'distribution': 'North America'}
    }
    map_html = mock_backend.tree_map()
    for tree_name, tree_data in tree_locations.items():
        assert str(tree_data['location'][0]) in map_html 
        assert str(tree_data['location'][1]) in map_html
        assert tree_data['distribution'] in map_html 

def test_tree_map_html_representation(mock_backend):
    map_html = mock_backend.tree_map()

    assert map_html.strip() != ''
    assert 'Coast Redwood' in map_html
    assert 'Ginko' in map_html
    assert 'Japanese Magnolia' in map_html
    assert 'Juniper' in map_html
    assert 'Live Oak' in map_html
    assert 'Monterey Cypress' in map_html
    assert 'Palm' in map_html
    assert 'Palmetto' in map_html
    assert 'Water Oak' in map_html
    assert 'White Oak' in map_html
    # assert 'Distribution Map' in map_html
    # assert '<i style="background-color:' in map_html
    # assert '<b style="font-size: 16px;">Distribution: </b>' in map_html

def test_tree_map_markers(mock_backend):
    tree_locations = {
        'Coast Redwood': {'location': (38.9822, -123.3781), 'distribution': 'North America'},
        'Ginko': {'location': (39.7684, -86.1581), 'distribution': 'East Asia'},
        'Japanese Magnolia': {'location': (35.8801, -79.0800), 'distribution': 'East Asia'},
        'Juniper': {'location': (40.7968, -77.8619), 'distribution': 'North America, Eurasia'},
        'Live Oak': {'location': (30.3894, -86.5229), 'distribution': 'North America'},
        'Monterey Cypress': {'location': (36.6002, -121.8947), 'distribution': 'North America'},
        'Palm': {'location': (26.7056, -80.0364), 'distribution': 'Africa, Eurasia, Americas'},
        'Palmetto': {'location': (26.7153, -81.0522), 'distribution': 'North America'},
        'Water Oak': {'location': (30.4383, -84.2807), 'distribution': 'North America'},
        'White Oak': {'location': (33.9860, -83.7185), 'distribution': 'North America'}
    }

    tree_names = ['Coast Redwood', 'Ginko', 'Japanese Magnolia', 'Juniper', 'Live Oak','Monterey Cypress', 'Palm', 'Palmetto', 'Water Oak', 'White Oak']
