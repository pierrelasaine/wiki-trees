from flask import render_template, abort
from google.cloud import storage


bucket_name = "wiki_content_p1"
storage_client = storage.Client.from_service_account_json("buckets-read-write-key.json")

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html")

    @app.route("/pages")
    def pages_index():
        # get a list of all the blobs in the bucket
        blobs = storage_client.list_blobs("wiki_content_p1")
        # render the template passing the blobs to pages.html
        return render_template("pages.html", pages=blobs)

    @app.route("/pages/<tree>")
    def page(tree):
        # retrieve blob
        blob = storage_client.bucket("wiki_content_p1").get_blob(f"{tree}.txt")
        # return Page not found if page not in buckets
        if not blob:
            abort(404)
        # get contents as byte string
        contents_bytes = blob.download_as_string()
        # decode to string
        contents = contents_bytes.decode("utf-8")
        # split contents into a list of lines
        lines = contents.splitlines()
        # pass the lines to the page template and return the page
        return render_template("page_template.html", lines=lines)

    @app.route("/about")
    def about():
        return render_template("about.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route('/signup')
    def new_user():
        return render_template("signup.html")

    @app.route('/login')
    def past_user():
        return render_template("login.html")