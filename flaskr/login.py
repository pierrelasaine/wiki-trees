from flaskr.user import User
from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user


# Solution: Moved from pages.py to use login_manager endpoint separately
def make_endpoints(app, login_manager, backend):
    # Solution: Required for login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route('/signup', methods=["GET", "POST"])
    def new_signup():
        pages = backend.get_all_page_names()
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if backend.sign_up(username, password):
                login_user(User(username))
                return redirect('/')
            else:
                return render_template("login.html",
                                       error_message="Username already exists!",
                                       active_tab='SignUp',
                                       pages=pages)
        else:
            return render_template("login.html",
                                   active_tab='SignUp',
                                   pages=pages)

    @app.route('/login', methods=["GET", "POST"])
    def user_login():
        pages = backend.get_all_page_names()
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if backend.sign_in(username, password):
                login_user(User(username))
                return redirect('/')
            else:
                return render_template(
                    "login.html",
                    error_message="Incorrect username or password!")
        else:
            return render_template("login.html", pages=pages)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))
