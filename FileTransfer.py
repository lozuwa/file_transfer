"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm Bolivia
Description: Class for the File Transfer program.
"""
# Libraries
# General purpose
import os
import sys
import logging
# Local libraries
from Database import Database
from utils import *

logging.basicConfig(level=logging.INFO) #format="%s(asctime)s:%(levelname)s:%s(message)s")

class Paths:
	"""
	Public static final class that defines constant paths.
	"""
	# TODO: set the correct path to DCMI in a smartphone
	PATH_TO_DEVICES = "c:/Users/HP/Downloads/origin/"
	PATH_TO_DESTINATION_IN_PC = "c:/Users/HP/Downloads/destination/"
	PATH_TO_DCIM_IN_PHONE = "DCIM"

class FileTransfer(Database):
	"""
	Copies files between to destinations and adds
	them to a database.
	"""
	def __repr__(self):
		return "FileTransfer({},{})".format(self.originPaths, self.destinationPath)

	def __init__(self):
		super().__init__()
		self.originPaths = None
		self.destinationPath = Paths.PATH_TO_DESTINATION_IN_PC
		# Assert destination path
		assert os.path.isdir(self.destinationPath) == True, "Path does not exist: {}".format(self.destinationPath)

	@property
	def propertyOriginPaths(self):
		"""
		Getter for originPaths.
		Returns:
			A list that contains the origin paths. If not set yet, then None.
		"""
		return self.originPaths

	@propertyOriginPaths.setter
	def propertyOriginPaths(self, connectedDevices):
		"""
		Setter for originPaths.
		Args:
			connectedDevices: A list that contains the names of the connected
								devices.
		Returns:
			None
		"""
		self.originPaths = connectedDevices

	def numberConnectedDevices(self):
		"""
		Checks the devices connected at the origin path.
		Returns:
			A list containing the devices connected if the list is over 0,
			otherwise return None.
		"""
		# Get the devices connected at origin path
		connectedDevices = os.listdir(Paths.PATH_TO_DEVICES)
		logging.info("Connected devices: {}".format(connectedDevices))
		return connectedDevices if len(connectedDevices) > 0 else None

	def comparePathWithDB(self):
		"""
		Compare the origin path and the db in order to obtain the missing folders.
		Returns:
			A list of tuples containing the path and the name of the folder that
			needs to be transfered.
		"""
		# Variables
		foldersOriginPathName = []
		foldersOriginPathPath = []
		returnFoldersAndPaths = []
		# Iterate over devices
		for path in self.originPaths:
			# Get folders in each device and iterate
			try:
				folders = os.listdir(path)
			except Exception as e:
				logging.error("Writer might be in use. Skipping reading.")
				continue
			for folder in folders:
				# Check if folder is in the db
				retrievedData = [i for i in self.read(folder)]
				# If the folder is found, then do nothing
				if len(retrievedData) > 0:
					continue
				# Otherwise, append to return list
				else:
					logging.info("Folder that needs to be copied: {}, {}".format(path, folder))
					returnFoldersAndPaths.append((path, folder))
		# Return the folders
		return returnFoldersAndPaths

	def transferFolder(self,
						folderName,
						folderPath):
		"""
		Transfer a folder from the origin path to the destination path.
		While transferring add the corresponding fields to the db.
		Args:
			folderNames: A string that contains the number of the folder to transfer.
			folderPath: A string that contains the path of the folder to transfer.
		Returns:
			None
		"""
		#try:
		# Move folder
		os.rename(os.path.join(folderPath, folderName),\
						os.path.join(Paths.PATH_TO_DESTINATION_IN_PC, folderName))
		# Insert to db
		dictToInsert = {"name": folderName,\
						"path": os.path.join(Paths.PATH_TO_DESTINATION_IN_PC, folderName),\
						"diagnostic": 0,\
						"results": []}
		self.create(dictToInsert = dictToInsert)
		#except:
		#	logging.warning("Impossible to transfer folder, writer is in use. Skipping folder.")

	@staticmethod
	def create_folder(folder_name):
		"""
		Creates a folder.
		Args:
			folder_name: A string that contains the name of the folder to be
						created.
		Returns:
			A boolean that contains the success state of the operation.
		"""
		# Variables
		result = False
		# Assert and create
		if os.path.isdir(folder_name):
			logging.debug("File already exists")
		else:
			try:
				os.mkdir(folder_name)
			except Exception as e:
				logging.error("File could not be created: {}".format(e))
			else:
				result = True
				logging.info("File created: {}".format(folder_name))
		return result

	@staticmethod
	def check_amount_of_files(folder_name):
		"""
		Checks how many files are in a specific folder
		Args:
			folder_name: input string that contains the path of the folder
							we are trying to count
		Returns:
			True if the folder has the correct amount of files
			False if the folder does not have the correct amount of files
		"""
		# Assertion
		assert os.path.isdir(folder_name), ": ERROR: folder does not exist: {}".\
												format(folder_name)
		# Count files
		files = os.listdir(folder_name)
		if len(files) == FILES_QUANTITY_THRESHOLD:
			logging.info("folder {} is available for transfer".format(folder_name))
			return True
		else:
			logging.info("folder: {} is not available for transfer. Amount of files: {}".\
							format(folder_name, len(files)))
			return False
