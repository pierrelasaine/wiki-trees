"""Creates and configures a Flask app for serving a wiki website."""

from flaskr import pages, login
from flaskr.backend import Backend
from flask import Flask
from flask_login import LoginManager

import logging

logging.basicConfig(level=logging.DEBUG)


# The flask terminal command inside "run-flask.sh" searches for
# this method inside of __init__.py (containing flaskr module
# properties) as we set "FLASK_APP=flaskr" before running "flask".
def create_app(test_config=None):
    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)

    # This is the default secret key used for login sessions
    # By default the dev environment uses the key 'dev'
    app.config.from_mapping(SECRET_KEY='dev', )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        # This file is not committed. Place it in production deployments.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # Solution code: modifying the additional endpoints
    backend = Backend()
    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    pages.make_endpoints(app, backend)
    login.make_endpoints(app, login_manager, backend)
    return app


"""
local GAE simulation command:
python2 /Users/pierrejohnson/google-cloud-sdk/.install/.backup/bin/dev_appserver.py app.yaml
"""
