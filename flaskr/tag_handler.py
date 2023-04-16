"""TagHandler for managing tags in a CSV file stored in Google Cloud Storage.

This module provides a TagHandler class to handle adding and retrieving tags
associated with filenames in a CSV file stored in a Google Cloud Storage bucket.
It allows users to add new filenames and tags to the CSV file, retrieve a list of
filenames associated with a given tag, and add new tags to existing filenames.

Example:
    from google.cloud import storage
    import csv
    import io

    tag_handler = TagHandler()
    tag_handler.add_file_to_csv("example.txt")
    tag_handler.add_tag_to_csv("example.txt", "new_tag")
    filenames = tag_handler.get_filenames_by_tag("new_tag")

Attributes:
    storage_client (google.cloud.storage.Client): Google Cloud Storage client object.
    dict_reader (csv.DictReader): CSV DictReader object for reading CSV data as dictionaries.
    dict_writer (csv.DictWriter): CSV DictWriter object for writing dictionaries as CSV data.
"""
from google.cloud import storage
import csv
import io


class TagHandler:
    """Handles adding and retrieving tags associated with filenames in a CSV file stored in Google Cloud Storage.

    Attributes:
        csv_filename (str): The name of the CSV file stored in the Google Cloud Storage bucket.
        storage_client (google.cloud.storage.Client): Google Cloud Storage client object.
        bucket (google.cloud.storage.Bucket): The Google Cloud Storage bucket where the CSV file is stored.
        blob (google.cloud.storage.Blob): The Google Cloud Storage blob representing the CSV file.
        dict_reader (csv.DictReader): CSV DictReader object for reading CSV data as dictionaries.
        dict_writer (csv.DictWriter): CSV DictWriter object for writing dictionaries as CSV data.
    """

    def __init__(self,
                 csv_filename="tags.csv",
                 storage_client=storage.Client(),
                 dict_reader=csv.DictReader,
                 dict_writer=csv.DictWriter):
        self.csv_filename = csv_filename
        self.storage_client = storage_client
        self.bucket = self.storage_client.bucket("wiki_content_p1")
        self.blob = self.bucket.blob(self.csv_filename)
        self.dict_reader = dict_reader
        self.dict_writer = dict_writer

    def open_file(self):
        """Opens the CSV file as a StringIO object.

        Returns:
            io.StringIO: StringIO object containing the CSV data.
        """
        return io.StringIO(self.blob.download_as_text())

    def get_filenames_by_tag(self, tag):
        """Get a list of filenames associated with a given tag.

        Args:
            tag (str): The tag to search for.

        Returns:
            list: A list of filenames associated with the given tag.
        """
        with self.open_file() as csvfile:
            reader = self.dict_reader(csvfile)
            filenames = []

            for row in reader:
                if tag in row["tags"]:
                    filenames.append(row["filename"])

        return filenames

    def add_tag_to_csv(self, filename, tag):
        """Add a new tag to the CSV file for a given filename.

        Args:
            filename (str): The filename to add the tag to.
            tag (str): The new tag to add.
        """
        with self.open_file() as csvfile:
            reader = self.dict_reader(csvfile)
            rows = list(reader)

            for row in rows:
                if row["filename"] == filename:
                    if row["tags"]:
                        existing_tags = row["tags"].split(", ")
                        existing_tags.append(tag)
                        updated_tags = list(set(existing_tags))
                        row["tags"] = ", ".join(updated_tags)
                        break
                    else:
                        row["tags"] = f"{tag}"
                        break

        updated_csv = io.StringIO()
        fieldnames = ["filename", "tags"]
        writer = self.dict_writer(updated_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

        updated_csv.seek(0)
        self.blob.upload_from_file(updated_csv, content_type="text/csv")

    def add_file_to_csv(self, filename):
        """Add a new filename entry to the CSV file if it does not already exist.

        Args:
            filename (str): The filename to add.
        """
        with self.open_file() as csvfile:
            reader = self.dict_reader(csvfile)
            rows = list(reader)

        filename_exists = False

        for row in rows:
            if row["filename"] == filename:
                filename_exists = True
                break

        if not filename_exists:
            rows.append({"filename": filename, "tags": filename})

            updated_csv = io.StringIO()
            fieldnames = ["filename", "tags"]
            writer = self.dict_writer(updated_csv, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

            updated_csv.seek(0)
            self.blob.upload_from_file(updated_csv, content_type="text/csv")
