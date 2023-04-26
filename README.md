# wiki-trees

This Flask web application is a simple Wiki platform that allows users to create, edit, and manage Wiki pages. The application also includes user authentication features, allowing users to sign up, log in, and log out. Furthermore, it allows users to manage tags associated with pages stored in Google Cloud Storage.

## Features

- User authentication (sign up, log in, log out)
- Create, edit, and delete Wiki pages
- Manage tags associated with filenames in Google Cloud Storage

## Installation

### Prerequisites

- Python 3.x
- Pip
- Virtualenv (optional, but recommended)

### Setup

1. Clone the repository:
'git clone https://github.com/pierrelasaine/wiki-trees
cd flask-wiki'

2. Install the required packages:
pip install -r requirements.txt

3. Run the application:
./run-flask.sh

The application should now be running on `http://127.0.0.1:5000/`.

## Usage

- Visit the homepage and sign up for an account.
- Log in to your account to create, edit, or delete Wiki pages.
- Manage tags associated with pages.

## Tests

To run tests, run pytest:
pytest

## Dependencies

This application uses the following packages:

- Flask==2.1.0
- Flask-Login==0.6.2
- google-cloud-storage==2.7.0
- pytest==6.2.5
- pytest-cov==2.11.1
- Jinja2==3.1.2
- MarkupSafe==2.1.2
- itsdangerous==2.1.2
- Werkzeug==2.2.2
- bleach==3.3.1
- folium==0.14.0

## License

This project is licensed under the MIT License. See the [LICENSE] file for details.
