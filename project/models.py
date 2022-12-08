from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())