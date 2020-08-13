from . import bp
from flask import current_app
from flask_login import current_user

@bp.before_request
def debug():
    print('current app', current_app)
    print('current user', current_user)
