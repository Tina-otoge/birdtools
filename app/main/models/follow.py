from datetime import datetime

from ... import db
from . import TwitterID

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(TwitterID)
    target = db.Column(TwitterID)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
