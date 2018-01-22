"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm Bolivia
Description: Class for the database.

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
# Database
from pymongo import *

class Database:
	"""
	Creates a connection to a database.
	"""
	def __init__(self):
		# Create a client
		client = MongoClient()
		# Bind the patient's collection
		db = client.pfm_patients
		self.db = db.pfm_patients

	def insert(self,
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
		retrieved_dict = self.db.find({"name": name})
		return retrieved_dict

	def update(self,
							name,
							update_dict):
		"""
		Updates an element in the db.
		Args:
			name: pair a string that contains the name of the value 
						to update.
			dict_to_insert: dictionary that contains the key: value
											pairs to update.
		Returns:
			A string that contains the response of the insertion operation.
		"""
		response = self.db.update_one({"name" = name}, \
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
