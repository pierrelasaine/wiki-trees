from google.cloud import storage
import hashlib
import csv
import io
from difflib import get_close_matches


class Backend:

    def __init__(self, storage_client=storage.Client()):
        # Solution Storage: uses storage client to make buckets that are
        # essentially hidden from the frontend
        self.page_bucket = storage_client.bucket("wiki_content_p1")
        self.login_bucket = storage_client.bucket("users_passwords_p1")
        self.image_bucket = storage_client.bucket("developer_images")

    def get_wiki_page(self, name):  #wiki_content_p1
        blob_name = name
        # Solution code: uses page_bucket and checks for None value
        blob = self.page_bucket.get_blob(blob_name)
        if blob is None:
            return "No page exists with this name"

        with blob.open("r") as f:
            return f.read()

    def get_all_page_names(self):
        self.pages = []
        # Solution code: uses page bucket and doesn't list image files
        for blob in self.page_bucket.list_blobs():
            if not blob.name.endswith(("png", "jpg", "jpeg", "csv")):
                self.pages.append(blob.name)
        return self.pages

    def upload(self, file, name, original_filename):
        bucket = self.page_bucket
        if (original_filename.endswith(("png", "jpg", "jpeg"))):
            bucket = self.image_bucket
        blob = bucket.get_blob(name)
        if blob is not None:
            blob.delete
        blob = bucket.blob(name)
        with blob.open('wb') as f:
            f.write(file)

    def sign_up(self, username, password):
        blob = self.login_bucket.blob(f"users/{username}")
        # blob = self.bucket.blob(username)
        if blob.exists():
            return False

        # Hash password
        hash_pword = hashlib.blake2b(password.encode()).hexdigest()

        user_blob = {"username": username, "hash_pword": hash_pword}
        blob.upload_from_string(str(user_blob))

        return True

    def sign_in(self, username, password):
        blob = self.login_bucket.blob(f"users/{username}")
        # blob = self.bucket.blob(username)
        if not blob.exists():
            return False

        get_pword = blob.download_as_string().decode()
        get_pword = eval(get_pword)
        user_pword = hashlib.blake2b(password.encode()).hexdigest()

        if get_pword["hash_pword"] == user_pword:
            return True
        else:
            return False

    def get_image(self, image_name):
        # Solution code: check for if blob is none
        blob = self.image_bucket.get_blob(image_name)
        if blob is None:
            return bytearray()

        with blob.open("rb") as image:
            f = image.read()
            b = bytearray(f)
            return b

    # Uses the difflib Python library(specifically the “get_close_matches” function)
    # to return page results that might be spelled incorrectly.
    def search(self, search_input):
        tag_handler = Backend.TagHandler()
        return set(
            get_close_matches(search_input, self.get_all_page_names()) +
            tag_handler.get_filenames_by_tag(search_input))

    class TagHandler:

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
            return io.StringIO(self.blob.download_as_text())

        def get_filenames_by_tag(self, tag):
            with self.open_file() as csvfile:
                reader = self.dict_reader(csvfile)
                filenames = []
                for row in reader:
                    if tag in row["tags"]:
                        filenames.append(row["filename"])
                return filenames

        def add_tag_to_csv(self, filename, tag):
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
            return

        def add_file_to_csv(self, filename):
            with self.open_file() as csvfile:
                reader = self.dict_reader(csvfile)
                rows = list(reader)
                for row in reader:
                    if row["filename"] == filename:
                        return

            rows.append({"filename": filename, "tags": filename})

            updated_csv = io.StringIO()
            fieldnames = ["filename", "tags"]
            writer = self.dict_writer(updated_csv, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

            updated_csv.seek(0)
            self.blob.upload_from_file(updated_csv, content_type="text/csv")
            return


# backend1 = Backend("wiki_content_p1")
# backend2 = Backend("developer_images")
# backend3 = Backend("users_passwords_p1")
#print(backend.get_wiki_page("ginkgo.txt"))
#print(backend.get_all_page_names())
#print(backend2.get_image("bulbasaur.jpeg"))
#print(backend1.search("malm"))
