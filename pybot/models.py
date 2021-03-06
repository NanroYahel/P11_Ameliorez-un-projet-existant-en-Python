from datetime import datetime
from pybot import db

class UserRequest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	request = db.Column(db.String(200), index=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	status = db.Column(db.Boolean)
