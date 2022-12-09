from flask_login import UserMixin
from sqlalchemy.sql import func

from main import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    todo_lists = db.relationship('List', backref='user', lazy=True)
    todo_lists_items = db.relationship('Item', backref='user', lazy=True)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    todo_list_items = db.relationship('Item', backref='todolist', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todo_list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    text = db.Column(db.String(1000))
    completed = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())