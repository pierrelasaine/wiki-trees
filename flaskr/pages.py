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
from flaskr.backend import *

storage_client = storage.Client()

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template("main.html")

    @app.route("/pages")
    def pages_index():
        pages = backend1.get_all_page_names()
        return render_template("pages.html", pages=pages)

    @app.route("/pages/<filename>")
    def page(filename):
        if not is_valid_blob("wiki_content_p1", filename):
            abort(404)
            
        lines = backend1.get_wiki_page(filename).splitlines()
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
        if not is_valid_blob("developer_images", filename):
            abort(404)

        image_data = backend2.get_image(filename)
        response = make_response(image_data)
        response.headers.set("Content-Type", "image/jpeg")
        return response

    @app.route('/signup', methods=["GET","POST"])
    def new_signup():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if backend1.sign_up(username, password):
                 return redirect(url_for("Login"))
            else:
                # return render_template("siggnup.html", error="Username already exists!")
                return render_template("login.html", error="Username already exists!")
        else:
            # return render_template("signup.html")
            return render_template("login.html")

    @app.route('/login', methods=["GET","POST"])
    def user_login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if backend1.sign_in(username, password):
    #             session["username"] = username
                return redirect(url_for("Upload", username=username))
            else:
                return render_template("login.html", error="Invalid username or password")

        else:
            return render_template("login.html")

    #     # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route('/upload', methods=["POST"])
    def upload_files():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            file = request.form["file"]

            if backend1.upload(username,password, file):
                session["file"] = file
                return redirect(url_for('File Uploaded'))
            else:
                return render_template("upload.html")
def is_valid_blob(bucket_name, filename):
    bucket = storage_client.bucket(bucket_name)
    if bucket.exists():
        blob = bucket.blob(filename)
        if blob.exists():
            return True

    return False
