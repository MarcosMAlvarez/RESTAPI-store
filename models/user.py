import sqlite3
from db import db

class UserModel(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)	# Estas son las columnas
	username = db.Column(db.String(80))				# que va a tener la tabla
	password = db.Column(db.String(80))				# __tablename__ = 'users'

	def __init__(self, username, password):			# Los nombres de los atributos 
		self.username = username 					# tienen que ser iguales a los nombres
		self.password = password 					# de las columnas definidas arriba

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()