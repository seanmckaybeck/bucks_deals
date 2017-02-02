import os
path = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = 'foobar'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
BOOTSTRAP_USE_MINIFIED = True
BOOTSTRAP_SERVE_LOCAL = True
PAGINATION = 15
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(path, 'data.db')
MAILGUN_API_KEY = ''
MAILGUN_DOMAIN = ''

