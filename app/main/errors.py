from . import bp
from flask import render_template


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def invalid_error(e):
    return render_template('500.html'), 500
