import importlib
import os
from flask import Blueprint, Flask
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .twitter import TwitterAPI

scheduler = APScheduler()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()

def init_blueprint(module, prefix=False, **kwargs):
    name = module[len(__name__) + 1:]
    if prefix:
        kwargs['url_prefix'] = '/' + module.split('.')[-1]
    return Blueprint(name, module,
        static_folder='static',
        template_folder='templates',
        **kwargs,
    )

def schedule_daily(func, id=None, now=True):
    # if now:
    #     func()
    id = id or func.__name__
    scheduler.add_job(id, func, trigger='cron', minute='*')

def create_app(config_path='../birdtools.cfg'):
    os.environ['CONFIG_FILE'] = os.environ.get('CONFIG_FILE', config_path)
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_envvar('CONFIG_FILE')
    login.init_app(app)
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    TwitterAPI.init_app(app)
    scheduler.init_app(app)

    for module in ['main', 'auth']:
        module = importlib.import_module('{}.{}'.format(__name__, module))
        app.register_blueprint(module.bp)

    scheduler.start()

    return app
