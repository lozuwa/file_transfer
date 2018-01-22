"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm
Description: Variables and support methods
"""
# General purpose
import os
import sys
import time
# Impy
from impy.preprocess import preprocessImage
prep_img = preprocessImage()

#### Constant static variables
# Serial port
PORT_NUMBER = 0

# MQTT Variables
IP = "192.168.0.107"
PORT = 1883
KEEP_ALIVE_TIMING = 15

#### Assertion messages
VARIABLE_IS_NOT_STR = "Variable type is not str"
VARIABLE_IS_NOT_INT = "Variable type is not int"
VARIABLE_IS_NOT_BOOL = "Variable type is not bool"

################## MQTT topics ##################
PREFIX = "/40X/1"
# Microscope
MICROSCOPE_TOPIC = "/microscope{}".format(PREFIX)
# Camera app
CAMERA_APP_TOPIC = "/cameraApp{}".format(PREFIX)
# Autofocus app
AUTOFOCUS_APP_TOPIC = "/autofocusApp{}".format(PREFIX)
# Remote controller
REMOTE_CONTROLLER_TOPIC = "/remoteControllerApp{}".format(PREFIX)
# Macros
MACROS_TOPIC = "/macros{}".format(PREFIX)

################## MQTT messages ##################
# AUTOFOCUS_APP_TOPIC
GET_VARIANCE = "get;variance;{};None;None"
CLASSIFY_PATCHES = "classify;patches;None;None;None"

COMPLETE_SERVICE_MANUAL_CONTROLLER = "service;autofocus;completed;ManualControllerAndCamera;None"
COMPLETE_SERVICE_AUTOMATIC_CONTROLLER = "service;autofocus;completed;CameraActivity;None"

AUTOFOCUS_START_AUTOFOCUSACTIVITY = "autofocusApp;AutofocusActivity;start;None;None"
REQUEST_SERVICE_AUTOFOCUS_MANUAL = "requestService;autofocus;ManualController;None;None"
REQUEST_SERVICE_AUTOFOCUS_AUTOMATIC = "requestService;autofocus;AutomaticController;None;None"

# CAMERRA_APP_TOPIC
START_CAMERA_ACTIVITY = "cameraApp;start;CameraActivity;None;None"
EXIT_AUTOMATIC_CONTROLLER = "exit;AutomaticController;CreatePatient;None;None"
TAKE_PICTURE_AUTOMATIC = "takePicture;None;None;None;sample{}"

# MACROS_TOPIC
CHECK_BATTERY_STATUS = "listener;battery;status;None;None"

ACTIVATE_CHARGE = "charge;smartphone;activate;None;None"
DEACTIVATE_CHARGE = "charge;smartphone;deactivate;None;None"

# OTHERS
HANDSHAKE_WITH_LISTENER = "cameraApp;handshake;listener;40X;None"

HANDSHAKE_CAMERA_APP = "listener;handshake;cameraApp;40X;None"
HANDSHAKE_AUTOFOCUS_APP = "listener;handshake;autofocusApp;None;None"

################## ACTUATORS CONSTANT VARIABLES ##################
# Directions
DIRECTION_Y_UP = 1
DIRECTION_Y_DOWN = 0

DIRECTION_X_LEFT = 0
DIRECTION_X_RIGHT = 1

DIRECTION_Z_UP = 0
DIRECTION_Z_DOWN = 1

# Amount of steps
STEPS_Z = 100
STEPS_X = 10
STEPS_Y = 10

# Timings
TIME_Z = 1000
TIME_X = 3000
TIME_Y = 3000

##################### MACROS ##############################
TIMING_MACRO = 1000
STEPS_X_LEFT_MACRO = 180
STEPS_Y_UP_MACRO = 400

##################### AUTOFOCUS ###########################
# AMOUNT OF STEPS SCANNING
STEPS_PRECISION_FOR_AUTOFOCUS_SCANNING = 100
# AMOUNT OF STEPS CONVERGING
STEPS_PRECISION_FOR_AUTOFOCUS_CONVERGING = 85

# AMOUNT OF STEPS CALIBRATION BOLTS
STEPS_PRECISION_FOR_CALIBRATION_BOLTS = 250

# TIMINGS
TIMING_STEPS_AUTOFOCUS_SCANNING = 500

# CONVERGENCE COEFFICIENT INITIAL VALUE
CONVERGENCE_COEFFICIENT_INITIAL_VALUE = 5

# CONVERGENCE COEFFICIENT INCREASE
CONVERGENCE_COEFFICIENT_INCREASE = 1

# AUTOFOCUS START NUMBER OF FIELDS
INITIAL_FIELDS_TO_AUTOFOCUS = 20

# AMOUNT OF FIELDS TO ADD UNTIL TRIGGERING AUTOFOCUS
# SERVICE AGAIN
AUTOFOCUS_FIELDS_INCREASE_RATE = 80

# AUTOFOCUS EQUATION CONSTANTS
GAMMA = 25

# CONVERGENCE THRESHOLD WHEN TOO MANY SCANNING STEPS
CONVERGENCE_THRESHOLD_WHEN_TOO_MANY_STEPS = 40

######################## AUTOMATIC ########################
# Timing XY
AUTOMATIC_X_TIMING = 2000
AUTOMATIC_Y_TIMING = 2000

# Steps XY
AUTOMATIC_Y_STEPS = 10
AUTOMATIC_X_STEPS = 30

# Amount of fields per row
FIELDS_PER_ROW = 40

# Amount of fields to analyse
FIELDS_TO_ANALISE = 800

######################## FILE SYNC ########################
PATH_TO_FOLDERS_IN_PHONE = "c:/Users/HP/Downloads/origin/"
PATH_TO_DESTINATION_IN_PC = "c:/Users/HP/Downloads/destination/"

FILES_QUANTITY_THRESHOLD = 3

######################## SUPPORT FUNCTIONS ########################
def create_folder(folder_name):
	"""
	Creates a folder.
	Args:
		folder_name: string that contains the name
	Returns:
		a boolean that informs if the creation was succesful
	"""
	if os.path.isdir(folder_name):
		print(": INFO: Folder already exists")
	else:
		try:
			os.mkdir(folder_name)
		except:
			print("Folder could not be created")
			return False
	return True

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
		print(": INFO: folder {} is available for transfer".format(folder_name))
		return True
	else:
		print(": INFO: folder: {} is not available amount of files: {}".\
						format(folder_name, len(files)))
		return False

def crop_image_into_rois(image):
	"""
	Crops an image.
	Args:
		image: opencv tensor with
	Returns:
		a list containing the crops
	"""
	height, width, depth = image.shape
	cropped_regions = [] #prep_img.divide_into_patches()
	return cropped_regions
