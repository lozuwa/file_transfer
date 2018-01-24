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
		# Assert dictToInsert is a dictionary
		assert type(dictToInsert) == dict, "dictToInsert is not a dict"
		self.db.insert_one(dictToInsert)

	def read(self,
			key,
			value):
		"""
		Reads an element in the db.
		Args:
			key: A string that contains the key to filter in the db.
			value: A string that contains the value mapped to the key to find
					in the db.
		Returns:
			A list that contains a dictionary which holds the filtered value if
			there is data retrieved. Otherwise, return None.
		"""
		# Assert key and value are strings
		assert type(key) == str, "Key is not a str"
		assert type(value) == str, "Key is not a str"
		readData = [i for i in self.db.find({key: value})]
		return readData if len(readData) > 0 else None

	def update(self,
				key,
				value,
				dictToInsert):
		"""
		Updates an element in the db.
		Args:
			key: A string that contains the key to filter in the db.
			value: A string that contains the value mapped to the key to find
					in the db.
			updateDict: dictionary that contains the key: value
											pairs to update.
		Returns:
				A boolean that contains the response of the operation.
		"""
		# Assert key and value are strings. Assert dictToInsert is a dictionary
		assert type(key) == str, "Key is not a string"
		assert type(value) == str, "Value is not a string"
		assert type(dictToInsert) == dict, "dictToInsert is not a dictionary"
		response = self.db.update_one({key: value},\
										{"$set": dictToInsert})
		return bool(response["n"])

	def push(self,
				key,
				value,
				dictToInsert):
		"""
		Deletes one element in the database.
		Args:
			key: A string that contains the key to filter in the db.
			value: A string that contains the value mapped to the key to find
					in the db.
		Returns:
				A boolean that contains the response of the operation.
		"""
		assert type(key) == str, "Key is not a string"
		assert type(value) == str, "Value is not a string"
		assert type(dictToInsert) == dict, "dictToInsert is not a dictionary"
		response = self.db.update_one({key: value},\
										{"$push": dictToInsert})
		return bool(response["n"])

	def delete(self,
				key,
				value):
		"""
		Deletes one element in the database.
		Args:
			key: A string that contains the key to filter in the db.
			value: A string that contains the value mapped to the key to find
					in the db.
		Returns:
			A string with the result of the delete operation.
		"""
		# Assert key value
		assert type(key) == str, "Key is not a string"
		assert type(value) == str, "Value is not a string"
		self.db.remove({key: value})

	def extractAllDataPoints(self):
		"""
		Retrieves all the elements in the database.
		Returns:
			A list containing all the data points in the db.
		"""
		dataPoints = [i for i in self.db.find()]
		return dataPoints
