from functools import wraps
from flask import current_app, request
import tweepy

class TwitterAPI():
    api_key = None
    api_secret = None

    @classmethod
    def init_app(cls, app):
        with app.app_context():
            cls.api_key, cls.api_secret = app.config['TWITTER_API_KEY'], app.config['TWITTER_API_SECRET']

    def __init__(self, access_token=None, consumer_token=None):
        if access_token:
            auth = self.__class__._get_oauth()
            self.key, self.secret = access_token
            auth.set_access_token(self.key, self.secret)
        else:
            consumer_token = consumer_token or (
                current_app.config['TWITTER_API_KEY'],
                current_app.config['TWITTER_API_SECRET'],
            )
            auth = tweepy.AppAuthHandler(*consumer_token)
        self.api = tweepy.API(auth)

    @staticmethod
    def _get_oauth():
        return tweepy.OAuthHandler(
            current_app.config['TWITTER_API_KEY'],
            current_app.config['TWITTER_API_SECRET'],
            current_app.config.get('CALLBACK_URL'),
        )

    @classmethod
    def method(cls, func):
        @wraps(func)
        def partial(*args, **kwargs):
            return func(args[0], cls.from_app(), *args[1:], **kwargs)
        return partial

    @classmethod
    def from_request(cls):
        oauth_token = request.args.get('oauth_token'), request.args.get('oauth_verifier')
        if not all(oauth_token):
            return None
        return cls._from_oauth_token(*oauth_token).api

    @classmethod
    def from_cookies(cls):
        access_token = request.cookies.get('twitter_key'), request.cookies.get('twitter_secret')
        if not all(access_token):
            return None
        return cls(access_token=access_token).api

    @classmethod
    def from_config(cls):
        return cls(consumer_token=(cls.api_key, cls.api_secret)).api

    @classmethod
    def from_app(cls):
        if current_app:
            return cls().api
        return cls.from_config()

    @classmethod
    def _from_oauth_token(cls, token, secret):
        oauth_params = {
            'oauth_token': token,
            'oauth_token_secret': secret
        }
        auth = cls._get_auth()
        auth.request_token = oauth_params
        access_token = auth.get_access_token(oauth_params['oauth_token_secret'])
        return cls(access_token)

    @classmethod
    def get_login_url(cls):
        return cls._get_oauth().get_authorization_url()
