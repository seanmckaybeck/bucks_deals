import deta
from flask import Flask, current_app
from flask_admin import Admin, AdminIndexView
from flask_bootstrap import Bootstrap


# use this to create each deta.Base instance for each model db in views.py
db = deta.Deta()  # NOTE: this requires you to set the DETA_PROJECT_KEY env var to your project key
bootstrap = Bootstrap()
admin = Admin(template_mode='bootstrap3')


def create_app(config):
    global db
    app = Flask(__name__)
    app.config.from_pyfile(config)
    bootstrap.init_app(app)
    admin.init_app(app)
    from .views import deals_blueprint
    app.register_blueprint(deals_blueprint)
    return app
