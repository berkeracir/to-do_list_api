from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Resource, fields, Namespace

from main import db
from models import User


api = Namespace(name="auth", description="Authorization")

user_api_model = api.model('User', {
	'username': fields.String(required=True, description="Username", default="username"),
	'password': fields.String(required=True, description="User password", default="password")
})

change_password_api_model = api.model('User Change Password', {
	'password': fields.String(required=True, description="User password", default="password"),
	'new_password': fields.String(required=True, description="User new password", default="new_password")
})	# TODO: Should parameters be used? 

@api.route('/login')
class Login(Resource):
	'''Login'''

	@api.expect(user_api_model)
	@api.response(200, "Login Successful")
	@api.response(404, "User doesn't exist or wrong password!")
	def post(self):
		'''Logins the signed user with correct username and password'''
		
		username = api.payload['username']
		password = api.payload['password']

		user = User.query.filter_by(username=username).first()

		# check if the user actually exists and if user exists, take the user-supplied password, hash it, and compare it to the hashed password in the database
		if not user or not check_password_hash(user.password, password):
			api.abort(404, "User doesn't exist or wrong password!")

		# if the above check passes, then we know the user has the right credentials
		login_user(user)
		return '', 200


@api.route('/signup')
class SignUp(Resource):
	'''Signup'''

	@api.expect(user_api_model)
	@api.response(201, "Sign Up Successful")
	@api.response(404, "'Username cannot be empty!' or 'Username exists!'")
	def post(self):
		'''Signs up the user with given correct username and password'''
		
		# validate and add user to database
		username = api.payload['username']
		password = api.payload['password']

		if not username:	# if username field is empty, redirect back to signup page so user can try again
			api.abort(404, "Username cannot be empty!")

		user = User.query.filter_by(username=username).first()	# if this returns a user, then the username already exists in database

		if user:	# if a user is found, redirect back to signup page so user can try again
			api.abort(404, "Username exists!")

		# create a new user with the form data. Hash the password so the plaintext version isn't saved.
		new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

		# add the new user to the database
		db.session.add(new_user)
		db.session.commit()

		return '', 201


@api.route('/change_password')
class ChangePassword(Resource):
	'''Change Password'''

	@api.expect(change_password_api_model)
	@api.response(200, "Password Changed Successfully")
	@api.response(401, "Unauthorized")
	@api.response(404, "Wrong password!")
	@login_required
	def put(self):
		'''Changes authorized user's password'''

		password = api.payload['password']
		new_password = api.payload['new_password']
		
		# take the user-supplied password, hash it, and compare it to the hashed password in the database
		if not check_password_hash(current_user.password, password):
			api.abort(404, "Wrong password!")

		# change the password
		current_user.password = generate_password_hash(new_password, method='sha256')

		# update the user's information in the database
		db.session.add(current_user)
		db.session.commit()

		return '', 200


@api.route('/logout')
class Logout(Resource):
	'''Logout'''

	@api.response(200, "Logout Successful")
	@api.response(401, "Unauthorized")
	@login_required
	def get(self):
		'''Logouts the user'''

		logout_user()
		return '', 200