from .. import db
from ..twitter import TwitterAPI
from .models import User, Follow

def update_users_data():
    print('updating users data...')
    with db.app.app_context():
        api = TwitterAPI.from_config()
        for user in User.query.all():
            user.update(api=api)
        db.session.commit()
    print('users data updated.')
