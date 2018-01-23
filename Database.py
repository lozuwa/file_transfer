"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm Bolivia
Description: Creates a connection to the pfm_patients database and implements
the CRUD operations.

* dictionary template to introduce in db:
	{"name": "",
	"diagnostic": 0,
	"parasites": [],
	"count": []}
"""

# Libraries
# General purpose
import os
import sys
# Interface
from interface import implements
# Database
from pymongo import *
# Local Libraries
from CRUD import CRUD

class Database(implements(CRUD)):
	"""
	Creates a connection to a database.
	CRUD operations for the db.
	"""
	def __init__(self):
		# Assert mongodb is running
		assert os.system("ps -a | grep mongod") == 0, MONGOD_IS_NOT_RUNNING
		# Create a client
		client = MongoClient()
		# Bind the patient's collection
		db = client.pfm_patients
		self.db = db.pfm_patients

	def create(self,
				dictToInsert):
		"""
		Inserts an element to the db.
		Args:
			dictToInsert: dictionary that contains the key: value
											pairs to insert.
		Returns:
			A string that contains the response of the insertion operation.
		"""
		response = self.db.insert_one(dictToInsert)
		return response

	def read(self,
			name):
		"""
		Reads an element in the db.
		Args:
			name: A string that contains the name of the value to retrieve.
		Returns:
			A dictionary containing the filtered value.
		"""
		retrievedDict = self.db.find({"name": name})
		return retrievedDict

	def update(self,
				name,
				updateDict):
		"""
		Updates an element in the db.
		Args:
			name: pair a string that contains the name of the value
						to update.
			updateDict: dictionary that contains the key: value
											pairs to update.
		Returns:
			A string that contains the response of the insertion operation.
		"""
		response = self.db.update_one({"name": name}, \
																		{"$set": update_dict})
		return response

	def delete(self,
				name):
		"""
		Deletes one element in the database.
		Args:
			name: A string that contains the value to find and remove the
						data point in the db.
		Returns:
			A string with the result of the delete operation.
		"""
		self.db.remove({"name": name})

	def extractAllDataPoints(self):
		"""
		Retrieves all the elements in the database.
		Returns:
			A list containing all the data points in the db.
		"""
		dataPoints = [i for i in self.db.find()]
		return dataPoints
