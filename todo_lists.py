from flask_login import login_required, current_user
from flask_restx import Resource, fields, Namespace

from main import db
from models import User, List


api = Namespace(name="todo_lists", description="Management of To-Do Lists")

api_model = api.model('To-Do List', {
	'id': fields.Integer(readonly=True, description="id"),
	'name': fields.String(required=True, description="Name"),
	'created_at': fields.DateTime(readonly=True, description="Creation Date")
})

post_parser = api.parser()
post_parser.add_argument('name', required=True, type=str, help="Name of To-Do List")

put_parser = api.parser()
put_parser.add_argument('id', required=True, type=int, help="ID of To-Do List")
put_parser.add_argument('name', required=True, type=str, help="Name of the To-Do List")

delete_parser = api.parser()
delete_parser.add_argument('id', required=True, type=int, help="ID of To-Do List")


@api.route('/')
class ToDoLists(Resource):
	'''Shows all To-Do Lists of authorized user, and gives the user ability of creating, updating, deleting new To-Do Lists'''

	@api.marshal_list_with(api_model, code=200)
	@api.response(200, "Got To-Do Lists Successfully")
	@api.response(401, "Unauthorized")
	@login_required
	def get(self):
		'''Gets all To-Do Lists of authorized user'''

		todo_lists = List.query.filter_by(user_id=current_user.id).all()
		return list(map(lambda x: x.serialize(), todo_lists)), 200

	@api.expect(post_parser)
	@api.marshal_with(api_model, code=201)
	@api.response(201, "To-Do List Created Successfully")
	@api.response(401, "Unauthorized")
	@login_required
	def post(self):
		'''Creates a new To-Do List with given name'''

		args = post_parser.parse_args()
		name = args['name']
		new_todo_list = List(user_id=current_user.id, name=name)
		db.session.add(new_todo_list)
		db.session.commit()

		return new_todo_list.serialize(), 201

	@api.expect(put_parser)
	@api.marshal_with(api_model, code=200)
	@api.response(200, "To-Do List Updated Successfully")
	@api.response(401, "Unauthorized")
	@api.response(404, "Wrong To-Do List ID")
	@login_required
	def put(self):
		'''Updates the name of To-Do List with given ID'''

		args = put_parser.parse_args()
		id = args['id']
		new_name = args['name']

		todo_list = List.query.filter_by(id=id, user_id=current_user.id).first()	# if this returns a To-Do List, then given id exists in database

		if not todo_list:
			api.abort(404, "Wrong To-Do List ID")

		# change the name
		todo_list.name = new_name

		# update the To-Do List information in the database
		db.session.add(todo_list)
		db.session.commit()

		return todo_list.serialize(), 200


	@api.expect(delete_parser)
	@api.response(200, "To-Do List Deleted Successfully")
	@api.response(401, "Unauthorized")
	@api.response(404, "Wrong To-Do List ID")
	@login_required
	def delete(self):
		'''Deletes the To-Do List with given ID'''

		args = delete_parser.parse_args()
		id = args['id']

		todo_list = List.query.filter_by(id=id, user_id=current_user.id).first()	# if this returns a To-Do List, then given id exists in database

		if not todo_list:
			api.abort(404, "Wrong To-Do List ID")

		# delete the To-Do List information in the database
		db.session.delete(todo_list)
		db.session.commit()

		return '', 200