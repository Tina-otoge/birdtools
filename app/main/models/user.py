from functools import wraps
from flask_login import UserMixin, current_user, login_required
from flask import redirect

from ... import login
from ...twitter import TwitterAPI
from . import db, TwitterID, Follow

class User(UserMixin, db.Model):
    id = db.Column(TwitterID, primary_key=True)
    screen_name = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)
    followers_count = db.Column(db.Integer)
    followings_count = db.Column(db.Integer)
    mutuals_count = db.Column(db.Integer)
    _data = None

    def __repr__(self):
        return '<{0} {1.screen_name} #{1.id}>'.format(type(self).__name__, self)

    def update(self, api=None):
        api = api or TwitterAPI.from_app()
        self.screen_name = api.get_user(self.id).screen_name
        Follow.query.filter_by(source=self.id).delete()
        Follow.query.filter_by(target=self.id).delete()
        followers = api.followers_ids(self.id)
        followings = api.friends_ids(self.id)
        for follower in followers:
            db.session.add(Follow(source=follower, target=self.id))
        for following in followings:
            db.session.add(Follow(source=self.id, target=following))
        self.followers_count = len(followers)
        self.followings_count = len(followings)
        self.mutuals_count = len([x for x in followings if x in followers])

    def get_followers_ids(self):
        return [x.source for x in Follow.query.filter_by(target=self.id).all()]

    def get_followings_ids(self):
        return [x.target for x in Follow.query.filter_by(source=self.id).all()]

    def get_mutuals_ids(self):
        followers = self.get_followers_ids()
        return [x for x in self.get_followings_ids() if x in followers]

    @staticmethod
    def admin_required(func):
        @wraps(func)
        @login_required
        def partial(*args, **kwargs):
            if not current_user.is_admin:
                return 'User must be admin', 403
            return func(*args, **kwargs)
        return partial

@login.user_loader
def load_user(id):
    return User.query.get(id)

'''
class User(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    _data = None
    _aliases = {
        'followings_count': 'friends_count',
        'followers': 'get_followers_ids',
        'followings': 'get_followings_ids',
        'mutuals': 'get_mutuals_ids',
        'mutuals_count': 'get_mutuals_count',
    }
    _followers = None
    _followings = None
    _mutuals = None

    def __repr__(self):
        return '<{0} #{1.id} {1.screen_name}>'.format(type(self).__name__, self)

    def __getattr__(self, name):
        if name in self._aliases:
            print('Alias', name, 'found')
            result = getattr(self, self._aliases[name])
            if callable(result):
                return result()
            return result
        print(name, 'not found in user properties, proxying to Twitter user')
        if not self._data:
            print('user data empty, querying Twitter API')
            self._data = TwitterAPI().get_user(self.id)
        result = getattr(self._data, name)
        print('found by proxying:', result)
        if result is None:
            print('Nothing found, raising exception')
            raise AttributeError('No attribute ' + name)
        return result

    def get_followers_ids(self):
        print('c followers')
        if not self._followers:
            print('querying twitter')
            self._followers = TwitterAPI().followers_ids(self.id)
        return self._followers

    def get_followings_ids(self):
        print('c followings')
        if not self._followings:
            print('querying twitter')
            self._followings = TwitterAPI().friends_ids(self.id)
        print('got', self._followings)
        return self._followings

    def get_mutuals_ids(self):
        if not self._mutuals:
            # l1 = self.get_followers_ids()
            print('getting followings')
            l1 = self.get_followings_ids()
            print('getting followers')
            l2 = self.get_followers_ids()
            self._mutuals = []
            for x in l1:
                if x in l2:
                    self._mutuals.append(x)
        return self._mutuals

    def get_mutuals_count(self):
        return len(self.mutuals)

    @staticmethod
    def admin_required(func):
        @wraps(func)
        @login_required
        def partial(*args, **kwargs):
            if not current_user.is_admin:
                return 'User must be admin', 403
            return func(*args, **kwargs)
        return partial

    # @classmethod
    # @login.user_loader
    # def load_user(cls, id):
    #     return cls.query.get(int(id))

@login.user_loader
def load_user(id):
    print('loading user for LoginManager from id =', id)
    return User.query.get(id)
'''
