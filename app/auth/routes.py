from flask import flash, make_response, render_template, redirect, request, url_for
from flask_login import login_user
from werkzeug.urls import url_parse

from .. import db
from ..main.models import User
from ..twitter import TwitterAPI
from . import bp

@bp.route('/login')
def login():
    api = TwitterAPI.from_request() or TwitterAPI.from_cookies()
    if api:
        me = api.me()
        print(me)
        user = User(me.id_str)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        response = make_response(redirect(url_for('main.index')))
        response.set_cookie('twitter_key', api.key)
        response.set_cookie('twitter_secret', api.secret)
        return response
    return render_template('login.html', login_url=TwitterAPI.get_login_url())
