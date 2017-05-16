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
MAILGUN_DOMAIN = 'sandbox4eaa7c2777d8425488180004f1cfaac4.mailgun.org'
MAILGUN_ADMIN = 'seanmckaybeck@gmail.com'
MAILGUN_FROM = 'Mailgun <mailgun@{}>'.format(MAILGUN_DOMAIN)
EBAY_APP_ID = ''
ADMIN_CREDS = ('', '')
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

