from google.cloud import storage
import hashlib

# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self, bucket_name):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self, username, password):
        pass

    def sign_up(self, username, password):
        # hash_pword = hashlib.blake2b(password.encode()).hexdigest()

        # Checks if username exists
        blob = self.bucket.blob(f"{username}.json")
        if blob.exists():
            return False

        # # Create user
        # new_user = {"username": username, "password": hash_pword}
        # new_user_json = json.dumps(new_user).encode("utf-8")
        # blob.upload_from_string(new_user_json)

        return True

    def sign_in(self):
        pass

    def get_image(self):
        pass

