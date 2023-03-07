from google.cloud import storage

# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self):
        self.storage_client = storage.Client()
        self.pages = []
        for blob in self.storage_client.list_blobs("wiki_content_p1"):
            self.pages.append(blob.name.strip(".txt"))

        
    def get_wiki_page(self, name): #wiki_content_p1
        bucket_name = "wiki_content_p1"
        blob_name = name
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        with blob.open("r") as f:
            return f.read()

    def get_all_page_names(self):
        return self.pages

    def upload(self, blob):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass

backend = Backend()
#print(backend.get_wiki_page("ginkgo.txt"))
print(backend.get_all_page_names())