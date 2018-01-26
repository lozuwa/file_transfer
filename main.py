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
from Preprocess import Preprocess
#from LoadObjectDetectionModel import LoadObjectDetectionModel
from utils import *

logging.basicConfig(level=logging.INFO,
											format="%s(asctime)s:%(levelname)s:%s(message)s")

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
		# Create instance of Preprocess
		prep = Preprocess()
		# Create instance of LoadObjectDetectionModel
		#objectDetection = LoadObjectDetectionModel()
		# Loop until set() is called on the interrupt
		while not self.interrupt.isSet():
			# Query not diagnosed folders in db
			foldersNotDiagnosed = prep.queryFolders()
			logging.info("Folders available for diagnostic: {}".
											format(foldersNotDiagnosed))
			# Assert there are folders not diagnosed
			if foldersNotDiagnosed != None:
				# Iterate over folder paths
				for folderNotDiagnosed in foldersNotDiagnosed:
					# Extract key: values from folderNotDiagnosed
					folderPath = folderNotDiagnosed["path"]
					folderName = folderNotDiagnosed["id"]
					imagesAtFolder = folderNotDiagnosed["files"]
					# Create tmp folder if it does not exist
					result = FileTransfer.create_folder(
																			os.path.join(folderPath, "tmp"))
					# Make sure folder was created
					if result:
						# Iterate over the images in the folder
						for imageAtFolder in imagesAtFolder:
							# Extract fields
							imageName = imageAtFolder["file_name"]
							imageDiagnostic = imageAtFolder["diagnostic"]
							# If the image has not been diagnosed, then
							# diagnose it.
							if imageDiagnostic == "0":
								# Load image into an opencv tensor
								logging.info("Classifying image {}".format(imageName))
								assert os.path.isfile(os.path.join(folderPath, imageName)),\
																									"File does not exist"
								frame = cv2.imread(os.path.join(folderPath, imageName))
								# Crop the image into patches
								patchesCoordinates = prep.preprocessImage(frame)
								# Iterate over patches
								for patch in patchesCoordinates:
									# Decode patch
									iy, ix, y, x = patch
									# Create saving path for the patch
									pathToPatch = os.path.join(folderName, "tmp", "tmp.jpg")
									# Save patch
									cv2.imwrite(pathToPatch, frame[iy:y, ix:x, :])
									# Classify patch
									input_image_path = os.path.join(pathToPatch)
									result, information = False, None #objectDetection.classifyFile(input_image_path,
																										#		output_image_path)
									if result:
										# Extract information
										classes = information[0]
										scores = information[1]
										classesScores = {i:j for i,j in zip(classes, scores)}
										image = information[2]
										# Rewrite the image
										imagePath = os.path.join(folderPath, imageName)
										cv2.imwrite(imagePath, image)
										# Update the database with the results
										prep.updateImageInDB(imageName, classesScores)
									else:
										pass
							else:
								pass
					else:
						logging.error("tmp folder could not be created.")
			else:
				pass
			# Wait the interrupt
			self.interrupt.wait(12)

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
			connectedDevices = ft.numberConnectedDevicesAtOrigin()
			# If there are no connected devices, then check again later.
			if connectedDevices == None:
				pass
			# Otherwise, transfer the folders and files to free up space 
			# in the devices.
			else:
				# Set paths to origin path
				connectedDevices = [os.path.join(Paths.PATH_TO_DEVICES,
														i, Paths.PATH_TO_DCIM_IN_PHONE) for i in
														connectedDevices]
				ft.originPaths = connectedDevices
				# Read folders in origin path
				foldersOriginPath = ft.readFoldersAtOrigin()
				# Iterate over folders
				for folderOriginPath in foldersOriginPath:
					# Check if folder is in db
					#logging.info("Looking for: {}, {}".format("id", folderOriginPath[1]))
					retrievedData = ft.isFolderAtDB(folderOriginPath[1])
					# If the folder is in the db, then index the files
					if retrievedData != None:
						# Check files field has data dataPoints
						# Extract list of files from the retrievedData query
						filesInFolderDb = [i["file_name"] for i in retrievedData[0]["files"]]
						# Read files at origin path and filter jpgs
						filesFolderOrigin = [i for i in os.listdir(os.path.join(folderOriginPath[0],
														folderOriginPath[1])) if i.endswith(".jpg")]
						# Iterate over files
						for fileFolderOrigin in filesFolderOrigin:
							# Check if file is in db
							# If the file already exists, then print an overwriting
							# warning.
							#print(fileFolderOrigin, filesInFolderDb)
							if fileFolderOrigin in filesInFolderDb:
								logging.warning("File already exists {} ... removing file.".
																	format(fileFolderOrigin))
								os.remove(os.path.join(folderOriginPath[0],
														folderOriginPath[1],
														fileFolderOrigin))
							# Otherwise, move the file to the destination path
							else:
								# try:
								# Move file
								originPath = os.path.join(folderOriginPath[0],
																					folderOriginPath[1])
								targetPath = os.path.join(Paths.PATH_TO_DESTINATION_IN_PC,
																					folderOriginPath[1])
								response = ft.transferFile(originPath = originPath,
																					targetPath = targetPath,
																					fileName = fileFolderOrigin)
								if response:
									logging.info("File moved and inserted in db")
								else:
									logging.error("File could not be moved or inserted {}".
																					format(fileFolderOrigin))
								# except:
								# 	logging.error("File could not be moved  or inserted {}".
								# 														format(fileFolderOrigin))
					# Otherwise, create the folder and insert into db
					else:
						result = ft.create_folder(os.path.join(
																		Paths.PATH_TO_DESTINATION_IN_PC,
																		folderOriginPath[1]))
						if result:
							# Save into db
							insertDict = {"id": folderOriginPath[1],
														"path": os.path.join(Paths.PATH_TO_DESTINATION_IN_PC,
																								folderOriginPath[1]),
														"diagnostic": "0",
														"files": []}
							response = ft.insertFolderToDB(insertDict)
							if response:
								logging.info("Folder created and saved in the database.")
							else:
								logging.error("Folder was not created and saved. " + 
															"Retrying later ..")
						else:
							logging.error("Folder could not be created: {}".
														format(os.path.join(Paths.PATH_TO_DESTINATION_IN_PC,
																								folderOriginPath[1])))
			# Sleep for 3 seconds. If interrupt.set() is called, then the thread
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
