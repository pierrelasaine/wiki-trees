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

from flask import render_template, abort, session, request, redirect, url_for, make_response, send_file, g
from flaskr.backend import Backend

from google.cloud import storage


#Solution code: backend is an endpoint
def make_endpoints(app, backend):
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template("main.html")

    @app.route("/pages", methods=["GET", "POST"])
    def pages_index():
        if request.method == "POST":
            search_input = request.form["search_input"]

            results = backend.search(search_input)
            return render_template("search_results.html",
                                   search_input=search_input,
                                   results=results)
        else:
            pages = backend.get_all_page_names()
            return render_template("pages.html", pages=pages)

    @app.route("/pages/<filename>")
    def page(filename):
        page_content = backend.get_wiki_page(filename)
        return render_template("page_template.html",
                               page_content=page_content,
                               filename=filename)

    @app.route("/about")
    def about():
        authors = [("Pierre Johnson", "bulbasaur.jpeg"),
                   ("Ericka James", "charmander.jpeg"),
                   ("Jalen Richburg", "squirtle.jpeg")]
        return render_template("about.html", authors=authors)

    @app.route("/images/<filename>")
    def get_image(filename):
        image_data = backend.get_image(filename)
        response = make_response(image_data)
        response.headers.set("Content-Type", "image/jpeg")
        return response

    @app.route("/upload", methods=["GET", "POST"])
    def upload():
        if request.method == 'POST':
            file = request.files['file']
            # Solution: adding name from the form.
            # TODO: catch and propagate any errors that may occur from upload
            name = request.form['name']
            backend.upload(file.stream.read(), name, file.filename)
            backend.TagHandler.add_file_to_csv(name)
            return render_template("main.html")

        else:
            return render_template("upload.html")

    @app.route('/search-results')
    def search():
        return render_template("search_results.html")

    @app.route("/tags/<filename>/", methods=["POST"])
    def add_tag(filename):
        tag_handler = g.get("tag_handler", Backend.TagHandler())
        filename = filename.replace("%20", " ")
        tag = request.form['tag']
        tag_handler.add_tag_to_csv(filename, tag)
        return redirect(url_for("page", filename=filename))
