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
# Threads
import threading
# Local Libraries
from FileTransfer import FileTransfer
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
			# Otherwise, transfer the folders to free up space in the devices.
			else:
				# Set paths to origin path
				ft.propertyOriginPaths(connectedDevices = connectedDevices)
				# Get folders in origin path
				foldersAndPaths = ft.comparePathWithDB()
				missingFoldersName = [i[0] for i in foldersAndPaths]
				missingFoldersPath = [i[1] for i in foldersAndPaths]
				# Iterate over folders
				for i in range(len(missingFoldersName)):
					# Check if the amount of files is valid for transfer
					result = ft.check_amount_of_files(missingFoldersName[i])
					# If it is valid, then copy the folder.
					if result:
						ft.transferFolder(missingFoldersName[i],\
											missingFoldersPath[i])
					# Otherwise, skip the folder.
					else:
						pass
            # Sleep for 10 seconds. If interrupt.set() is called, then the thread
			# will be closed even if it is in the interrupt.wait().
            self.interrupt.wait(3)

if __name__ == "__main__":
	# Create instance of FileTransfer
	ft = FileTransfer(originPath = pass, destinationPath = pass)
	# Create instance of main thread
	mt = MainThread()
	# Run thread
	mem.run()
	# Interrupt thread
	#mt.interrupt.set()
