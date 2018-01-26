"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm
Description: Program that constantly queries the db to
extract the folders that have not been diagnosed yet.
Once the query is obtained a classification algorithm is
run on the folders. The results are written in the same path.
"""
# Libraries
# General purpose
import os
import sys
import logging
# Local libs
from Database import Database
from impy import preprocess
from utils import *

class Preprocess(object):
	"""
	docstring for Preprocess.
	"""
	def __init__(self):
		# Compose a database class
		self.db = Database()
		# Make an instance of the preprocess module
		self.prepImage = preprocess.preprocessImage()

	def preprocessImage(self,
											tensor = None):
		"""
		Preprocess an image by dividing it into small patches
		for later classification.
		Args:
				tensor: An opencv tensor that contains an image.
		Returns:
				A list of lists that contains the coordinates of the
				patches that the image has been divided into.
		"""
		# Assertions
		assert len(tensor.shape) == 3, "Tensor does not have 3 dimensions."
		# Local variables
		if tensor.shape == None:
			logging.warning("No image has been passed to preprocess image.")
			return None
		height, width, depth = tensor.shape
		patchesCoordinates, _, __ = self.prepImage.divideIntoPatches(width,
																									height,
																									padding = "VALID_FIT_ALL",
																									number_patches = (4, 3))
		return patchesCoordinates

	def updateImageInDB(self,
											imageName,
											classesScores):
		"""
		Update the 
		TODO: There has to be a result
		Args:
			imageName: A string that contains the name of the image.
			classesScores: A dictionary that contains the maps class:score
		Results:
			None
		"""
		insertDict = {"files": {"file_name": imageName,
														"diagnostic": "1",
														"results": classesScores}}
		self.db.update(operation = "set",
										key = "id",
										value = folderName,
										dictToInsert = insertDict)

	def queryFolders(self):
		"""
		Query all the not diagnosed folders in the db.
		Returns:
				A list that contains the paths of the folders that
				require to be diagnosed if that is the case. Otherwise,
				return None.
		"""
		foldersNotDiagnosed = self.db.read(key = "diagnostic",
																			value = "0")
		return foldersNotDiagnosed

	@staticmethod
	def extract_images_from_folder(folder_path):
		"""
		DEPRECATED
		Extracts images from a folder.
		Args:
				folder_path: A string that contains the path
										to a folder.
		Returns:
				A list that contains the path of the images inside
				the folder_path.
		"""
		# Init local variables
		allowed_files = []
		# Assertions
		assert os.path.isdir(folder_path) == True, "Folder does not exist."
		# Read files and filter images
		for file_ in os.listdir(folder_path):
			if file_.endswith(".jpg"):
				allowed_files.append(os.path.join(folder_path, file_))
			else:
				continue
		return allowed_files
