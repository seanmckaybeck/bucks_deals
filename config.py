import os
path = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = 'foobar'
BOOTSTRAP_USE_MINIFIED = True
BOOTSTRAP_SERVE_LOCAL = True
PAGINATION = 15
DEBUG = True
MAILGUN_API_KEY = ''
MAILGUN_DOMAIN = 'seanmckaybeck.com'
MAILGUN_ADMIN = 'seanmckaybeck@gmail.com'
MAILGUN_FROM = 'Mailgun <mailgun@{}>'.format(MAILGUN_DOMAIN)
EBAY_APP_ID = ''
ADMIN_CREDS = ('', '')
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
