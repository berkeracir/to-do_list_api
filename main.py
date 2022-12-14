import os
import secrets

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix


basedir = os.path.abspath(os.path.dirname(__file__))

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,
    title='TO-DO LIST API',
    version='1.0',
    description='To-Do List API with Python-Flask',
	contact='Berker Acir',
	contact_email='berkeracir159@gmail.com'
)

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

import models
with app.app_context():
	db.create_all()

@login_manager.user_loader
def load_user(user_id):
	# since the user_id is just the primary key of our user table, use it in the query for the user
	return models.User.query.get(int(user_id))

from auth import api as auth_ns
api.add_namespace(auth_ns)

from todo_lists import api as todo_lists_ns
api.add_namespace(todo_lists_ns)

from todo_list import api as todo_list_ns
api.add_namespace(todo_list_ns)


if __name__ == '__main__':
	app.run()