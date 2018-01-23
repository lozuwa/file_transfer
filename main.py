"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm
Description: File transfer program to move folders from one path to another.
Useful when needing to free up space in some external device that is acquiring
data.
"""
# Libraries
# General purpose
import os
import sys
import logging
# Regex
import re
# Threads
import threading
# Local Libraries
from FileTransfer import FileTransfer
from FileTransfer import Paths
from utils import *

logging.basicConfig(level=logging.INFO, format="%s(asctime)s:%(levelname)s:%s(message)s")

class MainThread(threading.Thread):
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
					logging.info("Looking for: {}, {}".format("id", folderOriginPath[1]))
					retrievedData = ft.read(key = "id",\
											value = folderOriginPath[1])
					# If the folder is in the db, then index the files
					if retrievedData != None:
						# Check files field has data dataPoints
						# Extract list of files from the retrievedData query
						filesInFolderDb = [i["file_name"] for i in retrievedData[0]["files"]]
						# Read files at origin path
						filesFolderOrigin = os.listdir(os.path.join(folderOriginPath[0],\
																folderOriginPath[1]))
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
							else:
								# Otherwise, move the file to the destination path
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
											"diagnostic": 0,\
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
	# Create instance of FileTransfer
	ft = FileTransfer()
	# Create instance of main thread
	mt = MainThread()
	# Run thread
	mt.run()
	# Interrupt thread
	#mt.interrupt.set()
