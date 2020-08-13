from .. import init_blueprint, schedule_daily

bp = init_blueprint(__name__)

from . import routes, handlers

from .jobs import update_users_data

schedule_daily(update_users_data)
