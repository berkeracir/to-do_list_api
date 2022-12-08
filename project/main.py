from flask import Blueprint
from flask_login import login_required, current_user

from . import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/profile')
@login_required
def profile():
	return f"Hello {current_user.username}"