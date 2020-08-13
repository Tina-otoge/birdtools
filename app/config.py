import os

def _get_bool(key, default=None, any=False):
    value = os.environ.get(key)
    if any:
        return value is not None
    return value.lower() in ['1', 'yes', 'true', 'enable', 'enabled', 'on']

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'sqlite:///../app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = _get_bool('DB_TRACK_MODIFICATIONS', any=True)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'please move to mastodon/ostatus')
    TWITTER_API_KEY = os.environ.get('TWITTER_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_SECRET')
    CALLBACK_URL = os.environ.get('CALLBACK_URL')
