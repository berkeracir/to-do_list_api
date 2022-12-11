from flask_login import login_required, current_user
from flask_restx import Resource, fields, Namespace, inputs

from main import db
from models import List, Item


api = Namespace(name="todo_list", description="Management of To-Do List")

api_model = api.model('To-Do List Item', {
	'id': fields.Integer(readonly=True, description="id"),
	'todo_list_id': fields.Integer(readonly=True, description="To-Do List ID"),
	'text': fields.String(required=True, description="Item Description"),
	'completed': fields.Boolean(required=True, description="Completed"),
	'created_at': fields.DateTime(readonly=True, description="Creation Date")
})

post_parser = api.parser()
post_parser.add_argument('text', required=True, type=str, help="Text of To-Do List Item")
post_parser.add_argument('completed', default=False, type=inputs.boolean, help="Completed")

put_parser = api.parser()
put_parser.add_argument('id', required=True, type=int, help="To-Do List Item ID")
put_parser.add_argument('text', default=None, type=str, help="Text of the To-Do List Item")
put_parser.add_argument('completed', default=None, type=inputs.boolean, help="Completed")

delete_parser = api.parser()
delete_parser.add_argument('id', required=True, type=int, help="To-Do List Item ID")


@api.route('<int:todo_list_id>')
@api.param('todo_list_id', 'To-Do List ID')
@api.response(401, "Unauthorized")
class ToDoLists(Resource):
	'''
	Shows all To-Do List Items of authorized user, and gives the ability of creating, updating and deleting new To-Do List Items to the user
	'''
	
	@api.marshal_list_with(api_model, code=200)
	@api.response(200, "To-Do List Items Retrieved Successfully")
	@api.response(404, "Wrong To-Do List ID")
	@login_required
	def get(self, todo_list_id):
		'''Gets authorized user's all To-Do List Items of To-Do List with given ID'''

		# if this returns a To-Do List, then given To-Do List ID exists in database
		todo_list = List.query.filter_by(id=todo_list_id, user_id=current_user.id).first()

		if not todo_list:
			api.abort(404, "Wrong To-Do List ID")

		return list(map(lambda x: x.serialize(), todo_list.items)), 200

	@api.expect(post_parser)
	@api.marshal_with(api_model, code=201)
	@api.response(201, "To-Do List Item Created Successfully")
	@api.response(404, "Wrong To-Do List ID")
	@login_required
	def post(self, todo_list_id):
		'''Creates a new To-Do List Item with given text and completed value'''
		
		# if this returns a To-Do List, then given To-Do List ID exists in database
		todo_list = List.query.filter_by(id=todo_list_id, user_id=current_user.id).first()

		if not todo_list:
			api.abort(404, "Wrong To-Do List ID")

		args = post_parser.parse_args()
		text, completed = args['text'], args['completed']
		new_todo_list_item = Item(user_id=current_user.id, todo_list_id=todo_list_id, text=text, completed=completed)
		db.session.add(new_todo_list_item)
		db.session.commit()

		return new_todo_list_item.serialize(), 201

	@api.expect(put_parser)
	@api.marshal_with(api_model, code=200)
	@api.response(200, "To-Do List Item Updated Successfully")
	@api.response(404, "'Wrong To-Do List ID' or 'Wrong To-Do List Item ID'")
	@login_required
	def put(self, todo_list_id):
		'''
		Updates the text, completed status of To-Do List Item with given ID 
		from the specified To-Do List
		'''

		args = put_parser.parse_args()
		id, text, completed = args['id'], args['text'], args['completed']
		print(text, completed)

		# if this returns a To-Do List, then given To-Do List ID exists in database
		todo_list = List.query.filter_by(id=todo_list_id, user_id=current_user.id).first()

		if not todo_list:
			api.abort(404, "Wrong To-Do List ID")

		# if this returns a To-Do List Item, then given id exists in database
		todo_list_item = Item.query.filter_by(id=id, user_id=current_user.id, todo_list_id=todo_list_id).first()

		if not todo_list_item:
			api.abort(404, "Wrong To-Do List Item ID")
			
		# update flag
		update = False
		if text != None:	# if text field is empty, do not change text
			todo_list_item.text = text
			update = True
		if completed != None:
			todo_list_item.completed = completed
			update = True

		# update the To-Do List information in the database
		if update:
			db.session.add(todo_list_item)
			db.session.commit()

		return todo_list_item.serialize(), 200

	@api.expect(delete_parser)
	@api.response(200, "To-Do List Item Deleted Successfully")
	@api.response(404, "'Wrong To-Do List ID' or 'Wrong To-Do List Item ID'")
	@login_required
	def delete(self, todo_list_id):
		'''
		Deletes the To-Do List Item with given ID from the specified To-Do List
		'''

		args = put_parser.parse_args()
		id = args['id']

		# if this returns a To-Do List, then given To-Do List ID exists in database
		todo_list = List.query.filter_by(id=todo_list_id, user_id=current_user.id).first()

		if not todo_list:
			api.abort(404, "Wrong To-Do List ID")

		# if this returns a To-Do List Item, then given id exists in database
		todo_list_item = Item.query.filter_by(id=id, user_id=current_user.id, todo_list_id=todo_list_id).first()

		if not todo_list_item:
			api.abort(404, "Wrong To-Do List Item ID")

		# delete the To-Do List Item in the database
		db.session.delete(todo_list_item)
		db.session.commit()

		return '', 200