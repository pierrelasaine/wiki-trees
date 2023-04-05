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

from flask import render_template, abort, session, request, redirect, url_for, make_response, send_file

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

            results = backend1.search(search_input)
            return render_template("search_results.html",
                            search_input=search_input,
                            results=results)
        else:
            pages = backend1.get_all_page_names()
            is_login, uname = check_logged_in()
            return render_template("pages.html",
                                pages=pages,
                                logged_in=is_login,
                                username=uname)

    @app.route("/pages/<filename>")
    def page(filename):
        page_content = backend.get_wiki_page(filename)
        return render_template("page_template.html", page_content=page_content)

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
            return render_template("main.html")

        else:
            is_login, uname = check_logged_in()
            return render_template("upload.html",
                                   logged_in=is_login,
                                   username=uname)

    @app.route('/signup', methods=["GET", "POST"])
    def new_signup():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if backend.sign_up(username, password):
                session['username'] = username
                session['logged_in'] = True
                return redirect('/')
            else:
                return render_template("login.html",
                                       error_message="Username already exists!",
                                       active_tab='SignUp')
        else:
            return render_template("login.html", active_tab='SignUp')

    @app.route('/login', methods=["GET", "POST"])
    def user_login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if backend.sign_in(username, password):
                session['username'] = username
                session['logged_in'] = True
                return redirect('/')
            else:
                return render_template(
                    "login.html",
                    error_message="Incorrect username or password!")
        else:
            return render_template("login.html")

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    @app.route('/search-results')
    def search():
        return render_template("search_results.html")


def is_valid_blob(bucket_name, filename):
    bucket = storage_client.bucket(bucket_name)
    if bucket.exists():
        blob = bucket.blob(filename)
        if blob.exists():
            return True

    return False

"""
        else:    
            return render_template("upload.html")

"""

