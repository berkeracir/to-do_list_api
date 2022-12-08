import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
	app = Flask(__name__)

	app.config['SECRET_KEY'] = 'super-duper-secret-key'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

	db.init_app(app)

	login_manager = LoginManager()
	login_manager.init_app(app)

	from . import models

	with app.app_context():
		db.create_all()

	@login_manager.user_loader
	def load_user(user_id):
		# since the user_id is just the primary key of our user table, use it in the query for the user
		return models.User.query.get(int(user_id))

	# blueprint for auth routes of app
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	# blueprint for non-auth parts of app
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app