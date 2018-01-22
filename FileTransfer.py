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

class FileTransfer(Database):
	"""
	Copies files between to destinations and adds 
	them to a database.
	"""
	def __init__(self,
								originPath = None,
								destinationPath = None):
		super().__init__()
		self.originPath = originPath
		self.destinationPath = destinationPath
	
	def comparePaths(self):
		"""
		Compare the origin and destination path and get the difference.
		Returns:
			A set containing the folders that are in the origin path but not
			in the destination path.
		"""
		# Folders in origin path
		foldersOriginPath = [i for i in os.listdir(self.originPath)]
		# Data points in db
		foldersDB = self.extractAllDataPoints()
		# Compare both
		missingFolders = set(foldersOriginPath).difference(foldersDB)
		return missingFolders

	def transferFolders(self,
										folderNames):
		"""
		Transfer the folders from the origin path to the destination path.
		While transferring adds the corresponding fields to the db.
		Args:
			folderNames: A list that contains the names of the folders to 
									copy to the destination.
		Returns:
			None
		"""
		# Iterate
		for folderName in folderNames:
			try:
				# Get paths
				folderOriginPath = os.path.join(self.originPath, folderName)
				folderDestinationPath = os.path.join(self.destinationPath,\
																							folderName)
				# Move folder
				os.rename(folderOriginPath, folderDestinationPath)
				# Insert to the db
				dictToInsert = {"name": folderName,\
												"path": folderDestinationPath\
												"diagnostic": 0,\
												"results": []}
				self.insert(dictToInsert = dictToInsert)
			except:
				print(": ERROR: Writer is in use, skipping folder.")


