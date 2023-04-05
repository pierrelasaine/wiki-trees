"""Defines a Flask application that serves a wiki website, allowing users to browse and upload text and image files.

The main functionality of the wiki is provided by four routes:
    The home route ("/") displays the main page of the wiki.
    The pages index route ("/pages") displays a list of all the pages in the wiki.
    The page detail route ("/pages/<filename>") displays the contents of a specific page.
    The about route ("/about") displays information about the authors of the wiki.

The module also defines two additional routes for user authentication:
    The signup route ("/signup") displays a form for new users to create an account.
    The login route ("/login") displays a form for existing users to log in to their account.

All routes use templates rendered with Flask's "render_template" function, and interact with a Google Cloud Storage bucket to retrieve and store data.
"""

from flask import render_template, abort, session, request, redirect, url_for, make_response, send_file, send_from_directory
from flaskr.backend import *
from io import BytesIO

#Solution code: backend is an endpoint
def make_endpoints(app, backend):
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():      
        return render_template("main.html")

    @app.route("/pages")
    def pages_index():
        pages = backend.get_all_page_names()
        return render_template("pages.html", pages=pages)

    @app.route("/pages/<filename>")
    def page(filename):
        page_content = backend.get_wiki_page(filename)
        if not page_content:
            abort(404)

        return render_template("page_template.html", 
                               filename=filename,
                               page_content=page_content)

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
        image_data = backend.get_image(filename)
        if not image_data:
            abort(404)

        response = make_response(image_data)
        response.headers.set("Content-Type", "image/jpeg")
        return response

    @app.route("/upload", methods=["GET", "POST"])
    def upload():
        if request.method != 'POST':
            return render_template("upload.html")

        name = request.form['name']
        content_str = request.form['content']
        if not content_str:
            file = request.files['file']
            backend.bucket_upload(name, file)
        else:
            content_bstr = content_str.encode()
            content = BytesIO(content_bstr)
            backend.bucket_upload(name, content)
        ## check for validation [Page Redirect R8.]
        return redirect(url_for('page', filename=name))