from flask import Blueprint

bp = Blueprint('blog', __name__)
from . import views, errors
from ..models import Permission


@bp.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
