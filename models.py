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

    def __repr__(self) -> str:
        return f"<User| id={self.id} username=\"{self.username}> created_at=\"{self.created_at}\">"


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    todo_list_items = db.relationship('Item', backref='todolist', lazy=True)

    def __repr__(self) -> str:
        return f"<To-Do List| id={self.id} user_id={self.user_id} name=\"{self.name}\" created_at=\"{self.created_at}\">"

    def serialize(self) -> dict:
        return {'id': self.id, 'name': self.name, 'created_at': self.created_at}


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todo_list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    text = db.Column(db.String(1000))
    completed = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<To-Do List Item| id={self.id} user_id={self.user_id} todo_list_id={self.todo_list_id} text=\"{self.text}\" completed={self.completed} created_at=\"{self.created_at}\">"
