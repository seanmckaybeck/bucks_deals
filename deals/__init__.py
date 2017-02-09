from flask import Flask, current_app
from flask_admin import Admin, AdminIndexView
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bootstrap = Bootstrap()
admin = Admin(template_mode='bootstrap3')


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    db.init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)
    from .views import deals_blueprint
    app.register_blueprint(deals_blueprint)
    return app

