from flask_restful import Resource

from models.store import StoreModel

class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json()
		else:
			return {'message': 'Tienda no encontrada'}, 404

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': f"Ya se encontrada una tienda con el nombre {name}"}

		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'message': "Un error ocurrio mientras se creaba la tienda"}, 500

		return store.json(), 201
			
	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()

		return {'message': f"Tienda {name} eliminada"}

class StoreList(Resource):
	def get(self):
		return {'stores': [store.json() for store in StoreModel.query.all()]}