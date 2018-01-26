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
from utils import *

class Database(implements(CRUD)):
	"""
	Creates a connection to a database.
	CRUD operations for the db.
	"""
	def __init__(self):
		# Assert mongodb is running
		assert os.system("ps -a | grep mongod") == 0,\
						MONGOD_IS_NOT_RUNNING
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
		# Insert
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
		# Read
		readData = [i for i in self.db.find({key: value})]
		return readData if len(readData) > 0 else None

	def update(self,
							operation = None,
							key = None,
							value = None,
							dictToInsert = None):
		"""
		Updates an element in the db.
		Args:
			key: A string that contains the key to filter in the db.
			value: A string that contains the value mapped to the key to 
							find in the db.
			updateDict: dictionary that contains the key: value
											pairs to update.
		Returns:
				A boolean that contains the response of the operation.
		"""
		# Initialize local variables
		if operation == None:
			operation = "set"
		# Assert key, value and operation are str.
		# Assert dictToInsert is a dictionary
		assert type(key) == str, "Key is not str"
		assert type(value) == str, "Value is not str"
		assert type(operation) == str, "Operation is not str"
		assert type(dictToInsert) == dict, "dictToInsert is not a dict"
		# Define if set or push
		if operation == "set":
			response = self.db.update({key: value},\
																		{"$set": dictToInsert})
		elif operation == "push":
			response = self.db.update({key: value},\
																		{"$push": dictToInsert})
		else:
			raise Exception("Operation is not valid: {}".format(operation))
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
		# Remove
		self.db.remove({key: value})
