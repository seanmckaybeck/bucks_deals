from flask import render_template

from .views import deals_blueprint


@deals_blueprint.app_errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@deals_blueprint.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@deals_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@deals_blueprint.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
