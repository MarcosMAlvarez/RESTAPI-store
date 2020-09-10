from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()	# A diferencia del get_json, solo toma los datos que 
	parser.add_argument('price',		# se definen en los argumentos
			type=float,
			required=True,
			help="this field cannot be left blank"
	)
	parser.add_argument('store_id',		
			type=int,
			required=True,
			help="Todo item necesita un store_id"
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': "item no encontrado"}, 404

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': f"Ya hay un item con el nombre {name}"}, 400   #400: bad request

		request_data = Item.parser.parse_args()

		item = ItemModel(name, **request_data)

		try:
			item.save_to_db()
		except:
			return {'message': "ocurrio un error insertando el item"}, 500   # 500: Internal server error
		
		return {'message': f"se cargo exitosamente el item {item.json()}"}, 201  # 201: creado

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': f"Se ha eliminado el item {name}"}

	def put(self, name):
		request_data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		
		if item is None:
			item = ItemModel(name, **request_data)
		else:
			item.price = request_data['price']

		item.save_to_db()

		return {'message': f"Se modifico el item {item.json()}"}


class ItemList(Resource):
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}
