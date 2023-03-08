from google.cloud import storage
import hashlib
# import json

# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)
        
    def get_wiki_page(self, name): #wiki_content_p1
        blob_name = name
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        
        with blob.open("r") as f:
            return f.read()

    def get_all_page_names(self):
        self.pages = []
        for blob in self.storage_client.list_blobs(self.bucket_name):
            self.pages.append(blob.name.strip(".txt"))
        return self.pages

    def upload(self, username, password):
        pass

    def sign_up(self, username, password):
        if self.bucket.blob(username).exists():
            return False

        # Hash password
        hash_pword = hashlib.blake2b(password.encode()).hexdigest()

        blob = self.bucket.blob(username)
        blob.upload_from_string(hash_pword)
        return True

    def sign_in(self, username, password):
        if self.bucket.blob(username).exists():
            return False

        get_pword = self.bucket.blob(username).download_as_string().decode()
        user_pword = hashlib.blake2b(password.encode()).hexdigest()

        if get_pword == user_pword:
            return True
        else:
            return False
        

    def get_image(self):
        pass

backend = Backend("wiki_content_p1")
#print(backend.get_wiki_page("ginkgo.txt"))
print(backend.get_all_page_names())