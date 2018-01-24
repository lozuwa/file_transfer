"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm
Description: File transfer program to move folders from one path to another.
Useful when needing to free up space in some external device that is acquiring
data.
# TODO: kill the threads from an external program
"""
# Libraries
# General purpose
import os
import sys
import logging
# Image manipulation
import cv2
# Regex
import re
# Threads
import threading
# Local Libraries
from FileTransfer import FileTransfer
from FileTransfer import Paths
from ClassifyFolders import ClassifyFolders
from utils import *

logging.basicConfig(level=logging.INFO, format="%s(asctime)s:%(levelname)s:%s(message)s")

class ClassifyDBThread(threading.Thread):
	"""
	Inherits from thread and keeps thread alive until
	calling instance.interrupt.set().
	"""
	def __init__(self):
		"""
		Constructor
		"""
		threading.Thread.__init__(self)
		# Instantiate interrupt
		self.interrupt = threading.Event()

	def run(self):
		"""
		Runs the thread until calling instance.interrupt.set().
		"""
		# Create instance of classify
		clf = ClassifyFolders()
		# Loop until set() is called on the interrupt
		while not self.interrupt.isSet():
			# Query not diagnosed folders in db
			pathsNotDiagnosed = clf.queryNotDiagnosed(key = "diagnostic", value = "0")
			# Assert there are folders not diagnosed
			if pathsNotDiagnosed != None:
				# Iterate over folder paths
				for pathNotDiagnosed in pathsNotDiagnosed:
					# Create tmp folder if it does not exist
					result = FileTransfer.create_folder(os.path.join(pathNotDiagnosed, "tmp"))
					# Make sure folder was created
					if result:
						# Get full path to images in the folder
						imagesNotDiagnosed = clf.extract_images_from_folder(pathNotDiagnosed)
						for imageNotDiagnosed in imagesNotDiagnosed:
							# Load image path into opencv tensor
							logging.info("Classifying image {}".format(imageNotDiagnosed))
							assert os.path.isfile(imageNotDiagnosed), "Image does not exit."
							frame = cv2.imread(imageNotDiagnosed)
							# Preprocess image
							patchesCoordinates = clf.preprocessImage(frame)
							# Save image's patches
							for patch in patches:
								# Decode patch
								iy, ix, y, x = patch
								# Create path to patch
								pathToPatch = os.path.join(pathNotDiagnosed, "tmp", "tmp.jpg")
								# Save patch
								cv2.imwrite(frame[iy:y, ix:x, :], pathToPatch)
								# Classify patch
								result = clf.classifyFile()
					else:
						logging.error("tmp folder could not be created.")
			else:
				pass
			# Wait the interrupt
			self.interrupt.wait(30)

class FileTransferThread(threading.Thread):
	"""
	Inherits from Thread and keeps a thread alive until
	calling instance.interrupt.set().
	"""
	def __init__(self):
		"""
		Constructor
		"""
		threading.Thread.__init__(self)
		# Instantiate interrupt
		self.interrupt = threading.Event()

	def run(self):
		"""
		Runs the thread until calling instance.interrupt.set().
		"""
		# Make instances
		ft = FileTransfer()
		# Loop until set() is called on the interrupt
		while not self.interrupt.isSet():
			# Read origin and get the connected devices
			connectedDevices = ft.numberConnectedDevices()
			# If there are no connected devices, then check again later.
			if connectedDevices == None:
				pass
			# Otherwise, transfer the folders and files to free up space in the devices.
			else:
				# Set paths to origin path
				connectedDevices = [os.path.join(Paths.PATH_TO_DEVICES, \
									i, Paths.PATH_TO_DCIM_IN_PHONE) for i in \
									connectedDevices]
				ft.originPaths = connectedDevices
				# Read folders in origin path
				foldersOriginPath = ft.readOriginFolders()
				# Iterate over folders
				for folderOriginPath in foldersOriginPath:
					# Check if folder is in db
					#logging.info("Looking for: {}, {}".format("id", folderOriginPath[1]))
					retrievedData = ft.read(key = "id", value = folderOriginPath[1])
					# If the folder is in the db, then index the files
					if retrievedData != None:
						# Check files field has data dataPoints
						# Extract list of files from the retrievedData query
						filesInFolderDb = [i["file_name"] for i in retrievedData[0]["files"]]
						# Read files at origin path and filter jpgs
						filesFolderOrigin = [i for i in os.listdir(os.path.join(folderOriginPath[0],\
											folderOriginPath[1])) if i.endswith(".jpg")]
						# Iterate over files
						for fileFolderOrigin in filesFolderOrigin:
							# Check if file is in db
							# If the file already exists, then print an overwriting
							# warning.
							print(fileFolderOrigin, filesInFolderDb)
							if fileFolderOrigin in filesInFolderDb:
								logging.warning("File already exists {} ... removing file.".format(fileFolderOrigin))
								os.remove(os.path.join(folderOriginPath[0],\
														folderOriginPath[1],\
														fileFolderOrigin))
							# Otherwise, move the file to the destination path
							else:
								try:
									# Move file
									os.rename(os.path.join(folderOriginPath[0],\
															folderOriginPath[1],\
															fileFolderOrigin),\
											os.path.join(Paths.PATH_TO_DESTINATION_IN_PC,\
														folderOriginPath[1],\
														fileFolderOrigin))
									# Append to files in its corresponding folder
									insertDict = {"files": {"file_name": fileFolderOrigin}}
									ft.push(key = "id",\
											value = folderOriginPath[1],\
											dictToInsert = insertDict)
									logging.info("file moved and inserted in db")
								except:
									logging.error("File could not be moved {}".format(fileFolderOrigin))
					else:
						# Otherwise, create the folder and insert into db
						result = ft.create_folder(os.path.join(Paths.PATH_TO_DESTINATION_IN_PC,\
																folderOriginPath[1]))
						if result:
							# Save into db
							insertDict = {"id": folderOriginPath[1],\
											"path": os.path.join(Paths.PATH_TO_DESTINATION_IN_PC, folderOriginPath[1]),\
											"diagnostic": "0",\
											"files": []}
							ft.create(dictToInsert = insertDict)
							logging.info("Folder created and saved in the database.")
						else:
							logging.error("Folder could not be created: {}".format(os.path.join(Paths.PATH_TO_DESTINATION_IN_PC,\
																								folderOriginPath[1])))
			# Sleep for 10 seconds. If interrupt.set() is called, then the thread
			# will be closed even if it is in the interrupt.wait().
			self.interrupt.wait(3)
			#mt.interrupt.set()

if __name__ == "__main__":
	# Create instance of file transfer thread
	ftt = FileTransferThread()
	# Run thread
	ftt.start()
	# Interrupt thread
	#mt.interrupt.set()
	# Create instance of classify thread
	clft = ClassifyDBThread()
	# Run thread
	clft.start()
	# Interrupt thread
	#mt.interrupt.set()
    # Wait for threads to finish
	ftt.join()
	clft.join()
