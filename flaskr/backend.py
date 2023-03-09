from google.cloud import storage
import hashlib

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

    def upload(self, file):
        blob = self.bucket.blob(f"uploaded_content/{file}")
        if blob:
            return False

        blob.upload_from_file(file)
        return True
    def sign_up(self, username, password):
        blob = self.bucket.blob(f"users/{username}")
        # blob = self.bucket.blob(username)
        if blob.exists():
            return False

        # Hash password
        hash_pword = hashlib.blake2b(password.encode()).hexdigest()

        user_blob = {"username": username, "hash_pword": hash_pword}
        blob.upload_from_string(str(user_blob))

        return True

    def sign_in(self, username, password):
        blob = self.bucket.blob(f"users/{username}")
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
        blob = self.bucket.blob(f"wiki_content_p1")
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob)
        
        with blob.open("rb") as image:
            f = image.read()
            #b = bytearray(f)
            return f



backend1 = Backend("wiki_content_p1")
backend2 = Backend("developer_images")
backend3 = Backend("users_passwords_p1")
#print(backend.get_wiki_page("ginkgo.txt"))
#print(backend.get_all_page_names())
#print(backend2.get_image("bulbasaur.jpeg"))