"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm Bolivia
Description: Create, update, read and delete
interface for a database.
"""
# Libraries
from interface import Interface

class CRUD(Interface):
	"""
	Interface that contains all the methods that every database
	should implement.
	"""
	def create(self, 
						dictToInsert):
		pass

	def read(self, 
						key, 
						value):
		pass

	def update(self,
							operation = None, 
							key = None, 
							value = None, 
							dictToInsert = None):
		pass

	def delete(self, 
							key, 
							value):
		pass
