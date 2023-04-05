from google.cloud import storage
from flask import abort
from bleach import Cleaner
import hashlib


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
        blob = self.page_bucket.blob(blob_name)
        if blob is None:
            return None

        return blob.download_as_text()

    def get_all_page_names(self):
        self.pages = []
        # Solution code: uses page bucket and doesn't list image files
        for blob in self.page_bucket.list_blobs():
            if not blob.name.endswith(("png", "jpg", "jpeg")):
                self.pages.append(blob.name)
        return self.pages

    def upload(self, file, name, original_filename):
        bucket = self.page_bucket
        if (original_filename.endswith(("png", "jpg", "jpeg"))):
            bucket = self.image_bucket
        blob = bucket.blob(name)
        if blob.exists():
            blob.delete()
        blob.upload_from_file(file)

    def is_valid_html(self, html):
        """Checks if the given HTML string is safe.

        Args:
            html: A string containing HTML code.

        Returns:
            True if the HTML is safe, False otherwise.
        """
        cleaner = Cleaner(tags=[
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code', 'title',
            'div', 'em', 'i', 'li', 'ol', 'p', 'strong', 'u', 'ul', 'img'
        ],
                          attributes={
                              'a': ['href', 'title'],
                              'abbr': ['title'],
                              'acronym': ['title'],
                              'img': ['src', 'alt']
                          })

        sanitized_html = cleaner.clean(html)

        if sanitized_html != html:
            return False

        return True

    def tmd_html(self):
        pass

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

        get_pword = blob.download_as_bytes()
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


# backend1 = Backend("wiki_content_p1")
# backend2 = Backend("developer_images")
# backend3 = Backend("users_passwords_p1")
#print(backend.get_wiki_page("ginkgo.txt"))
#print(backend.get_all_page_names())
#print(backend2.get_image("bulbasaur.jpeg"))
