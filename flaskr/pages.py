"""Defines a Flask application that serves a wiki website, allowing users to browse and upload text and image files.

The main functionality of the wiki is provided by four routes:
    The home route ("/") displays the main page of the wiki.
    The pages index route ("/pages") displays a list of all the pages in the wiki.
    The page detail route ("/pages/<tree>") displays the contents of a specific page.
    The about route ("/about") displays information about the authors of the wiki.

The module also defines two additional routes for user authentication:
    The signup route ("/signup") displays a form for new users to create an account.
    The login route ("/login") displays a form for existing users to log in to their account.

All routes use templates rendered with Flask's "render_template" function, and interact with a Google Cloud Storage bucket to retrieve and store data.
"""

from flask import render_template, abort, session, request, redirect, url_for, make_response, send_file
from google.cloud import storage
from flaskr.backend import Backend

bucket_name = "wiki_content_p1"
storage_client = storage.Client()

backend = Backend(bucket_name)

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template("main.html")

    @app.route("/pages")
    def pages_index():
        blobs = storage_client.list_blobs(bucket_name)
        return render_template("pages.html", pages=blobs)

    @app.route("/pages/<tree>")
    def page(tree):
        blob = storage_client.bucket(bucket_name).get_blob(f"{tree}.txt")
        if not blob:
            abort(404)

        contents_bytes = blob.download_as_string()
        contents = contents_bytes.decode("utf-8")
        lines = contents.splitlines()
        return render_template("page_template.html", lines=lines)

    @app.route("/about")
    def about():
        authors = [
            ("Pierre Johnson", "bulbasaur.jpeg"),
            ("Ericka James", "charmander.jpeg"),
            ("Jalen Richburg", "squirtle.jpeg") 
        ]
        return render_template("about.html", authors=authors)

    @app.route("/images/<filename>")
    def get_image(filename):
        blob = storage_client.bucket("developer_images").get_blob(filename)
        if not blob:
            abort(404)

        image_data = blob.download_as_string()
        response = make_response(image_data)
        response.headers.set("Content-Type", "image/jpeg")
        return response

    @app.route('/signup', methods=["GET","POST"])
    def new_signup():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if backend.sign_up(username, password):
                 return redirect(url_for("login"))
            else:
                return render_template("signup.html", error="Username already exists!")
        else:
            return render_template("signup.html")

    @app.route('/login', methods=["GET","POST"])
    def user_login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if backend.sign_in(username, password):
                session["username"] = username
                # return redirect(url_for("upload"))
                return redirect(url_for("logged_in"))
            else:
                return render_template("login.html")

    #     # TODO(Project 1): Implement additional routes according to the project requirements.
