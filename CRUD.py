"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm Bolivia
Description: Creates a connection to the pfm_patients database and implements
the CRUD operations.
"""
# Libraries
from interface import Interface

class CRUD(Interface):
	"""
	Interface that contains all the methods that every database
	should implement.
	"""
	def create(self, dictToInsert):
		pass

	def read(self, key, value):
		pass

	def update(self, key, value, dictToInsert):
		pass

	def delete(self, key, value):
		pass
