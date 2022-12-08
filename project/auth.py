from flask import Blueprint, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
	username = request.args.get('username')
	password = request.args.get('password')

	user = User.query.filter_by(username=username).first()

	# check if the user actually exists and if user exists, take the user-supplied password, hash it, and compare it to the hashed password in the database
	if not user or not check_password_hash(user.password, password):
		return "User doesn't exist or wrong password!"

	# if the above check passes, then we know the user has the right credentials
	login_user(user) #, remember=remember) TODO
	return "Login Successful"

@auth.route('/signup', methods=['POST'])
def signup():
	# validate and add user to database
	username = request.args.get('username')
	password = request.args.get('password')

	if not username:	# if username field is empty, redirect back to signup page so user can try again
		return "Username cannot be empty!"

	user = User.query.filter_by(username=username).first()	# if this returns a user, then the username already exists in database

	if user:	# if a user is found, redirect back to signup page so user can try again
		return "Username exists!"

	# create a new user with the form data. Hash the password so the plaintext version isn't saved.
	new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

	# add the new user to the database
	db.session.add(new_user)
	db.session.commit()

	return "Signup Successful"

@auth.route('/change_password', methods=['POST'])
@login_required
def change_password():
	password = request.args.get('password')
	new_password = request.args.get('new_password')
	
	if not check_password_hash(current_user.password, password):
		return "Wrong password!"

	# change the password
	current_user.password = generate_password_hash(new_password, method='sha256')

	# update the new user to the database
	db.session.add(current_user)
	db.session.commit()

	return "Password Changed Successful"

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return "Logout Successful"