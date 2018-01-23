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
		logging.info("Origin paths set to: {}".format(ft.originPaths))

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

	def readOriginFolders(self):
		"""
		Reads the folders in the origin path.
		Returns:
			A list of tuples containing the (path, folder) names.
		"""
		# Variables
		foldersOriginPath = []
		# Iterate over paths
		for originPath in self.originPaths:
			try:
				# Read folders in path
				folders = os.listdir(originPath)
			except Exception as e:
				logging.error("Not able to read folders at path: {}".format(originPath))
				continue
			# Iterate over folders
			for folder in folders:
				foldersOriginPath.append((originPath, folder))
		# Return folders
		return foldersOriginPath

	def comparePathWithDB(self):
		"""
		Compare the origin path and the db in order to obtain the missing folders.
		Returns:
			Two lists:
			- A list of tuples containing the path and the name of the folder that
			needs to be transfered.
			- Another list of tuples containing the path and the name of the folder that
			already exist in the db.
		"""
		# Variables
		foldersOriginPathName = []
		foldersOriginPathPath = []
		missingFoldersAndPaths = []
		existingFoldersAndPaths = []
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
					existingFoldersAndPaths.append((path, folder))
				# Otherwise, append to return list
				else:
					logging.info("There is a folder that needs to be copied: {}, {}".format(path, folder))
					missingFoldersAndPaths.append((path, folder))
		# Return the folders
		return missingFoldersAndPaths, existingFoldersAndPaths

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
		try:
			# Move folder
			os.rename(os.path.join(folderPath, folderName),\
							os.path.join(Paths.PATH_TO_DESTINATION_IN_PC, folderName))
			# Insert to db
			dictToInsert = {"name": folderName,\
							"path": os.path.join(Paths.PATH_TO_DESTINATION_IN_PC, folderName),\
							"diagnostic": 0,\
							"results": []}
			self.create(dictToInsert = dictToInsert)
		except:
			logging.warning("Impossible to transfer folder, writer is in use. Skipping folder.")

	def transferFile(self,
					originPath,
					destinyPath,
					fileName):
		"""
		Transfer a file from path1 to path2.

		"""
		try:
			# Move file
			os.rename(os.path.join(originPath, fileName),\
						os.path.join(destinyPath, fileName))
			# Insert file in db
			dictToInsert = {"name": folderName,\
							"path": os.path.join(Paths.PATH_TO_DESTINATION_IN_PC, folderName),\
							"diagnostic": 0,\
							"results": []}
		except:
			pass

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
			logging.debug("Folder already exists")
			result = True
		else:
			try:
				os.mkdir(folder_name)
			except:
				logging.error("Folder could not be created: {}".format(e))
			else:
				result = True
				logging.info("Folder created: {}".format(folder_name))
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

	@staticmethod
	def extract_name_and_id(line):
		"""
		DEPRECATED
		Extracts a name and a consequent number.
		Args:
			line: A string that contains a name and a identification.
					E.g: rodrigo loza lucero_6729216
		Returns:
			A tuple that contains the filtered name and identification.
		"""
		name = re.match(r"([A-Za-z ]+)", line, re.I).group()
		identification = line.split("_")[1]
		return (name, identification)
