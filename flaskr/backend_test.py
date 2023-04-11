from flaskr.backend import Backend
from unittest.mock import MagicMock, patch
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import pytest
import csv
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
def mock_dict_reader():
    mock = MagicMock(spec=csv.DictReader)
    return mock


@pytest.fixture
def mock_dict_writer():
    mock = MagicMock(spec=csv.DictWriter)
    return mock


@pytest.fixture
def mock_client(mock_bucket):
    mock = MagicMock(spec=storage.Client)
    mock.bucket.return_value = mock_bucket
    return mock


@pytest.fixture
def mock_tag_handler(mock_client, mock_dict_reader, mock_dict_writer):
    mock = Backend.TagHandler("mock.csv", storage_client=mock_client, dict_reader=mock_dict_reader, dict_writer=mock_dict_writer)
    return mock


@patch("flaskr.backend.storage.Client")
def test_get_wiki_page(mock_client, mock_blob, mock_bucket, name):
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.get_blob.return_value = mock_blob

    mock_blob.open.return_value = io.StringIO("blob data")

    backend = Backend(mock_client)
    assert backend.get_wiki_page(name) == "blob data"


def test_get_filenames_by_tag_no_match(mock_tag_handler):
    mock_tag_handler.dict_reader.return_value = iter([{"filename": "file1", "tags": "tag1, tag2"},
                                                                                            {"filename": "file2", "tags": "tag1, tag3"}])
    assert mock_tag_handler.get_filenames_by_tag("mock") == []


def test_get_filenames_by_tag_match(mock_tag_handler):
    mock_tag_handler.dict_reader.return_value = iter([{"filename": "file1", "tags": "tag1, tag2"},
                                                      {"filename": "file2", "tags": "tag1, tag3"}])
    assert mock_tag_handler.get_filenames_by_tag("tag1") == ["file1", "file2"]

def test_add_tag_to_csv_invalid_filename(mock_tag_handler):
    mock_tag_handler.dict_reader.return_value = [{"filename": "file1", "tags": "tag1, tag2"}]
    mock_tag_handler.add_tag_to_csv("file2", "tag1")

    mock_tag_handler.dict_writer.return_value.writeheader.assert_called_once()
    mock_tag_handler.dict_writer.return_value.writerows.assert_called_once_with([{"filename": "file1", "tags": "tag1, tag2"}])


def test_add_tag_to_csv_no_tags(mock_tag_handler):
    mock_tag_handler.dict_reader.return_value = [{"filename": "file1", "tags": ""}]
    mock_tag_handler.add_tag_to_csv("file1", "tag1")

    mock_tag_handler.dict_writer.return_value.writeheader.assert_called_once()
    mock_tag_handler.dict_writer.return_value.writerows.assert_called_once_with([{"filename": "file1", "tags": "tag1"}])


def test_add_tag_to_csv(mock_tag_handler):
    mock_tag_handler.dict_reader.return_value = [{"filename": "file1", "tags": "tag1"}]
    mock_tag_handler.add_tag_to_csv("file1", "tag2")

    mock_tag_handler.dict_writer.return_value.writeheader.assert_called_once()
    try:
        mock_tag_handler.dict_writer.return_value.writerows.assert_called_once_with([{"filename": "file1", "tags": "tag1, tag2"}])
    except AssertionError:
        mock_tag_handler.dict_writer.return_value.writerows.assert_called_once_with([{"filename": "file1", "tags": "tag2, tag1"}])


def test_add_file_to_csv_existing_file(mock_tag_handler):
    mock_tag_handler.dict_reader.return_value = [{"filename": "file1", "tags": "tag1"}]
    mock_tag_handler.add_file_to_csv("file1")

    mock_tag_handler.dict_writer.return_value.writerow.assert_not_called()


def test_add_file_to_csv(mock_tag_handler):
    mock_tag_handler.dict_reader.return_value = [{"filename": "file1", "tags": "tag1"}]
    mock_tag_handler.add_file_to_csv("file2")

    mock_tag_handler.dict_writer.return_value.writerows.assert_called_once_with([{"filename": "file1", "tags": "tag1"}, {"filename": "file2", "tags": "file2"}])

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