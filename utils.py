"""
Author: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm
Description: Variables and support methods
"""
# Libraries
# General purpose
import os
import sys
import logging

logging.basicConfig(level=logging.INFO) #format="%s(asctime)s:%(levelname)s:%s(message)s")
# logging.basicConfig(level=logging.INFO, format="%s(asctime)s:%(levelname)s:%s(message)s")

######################## ASSERTION MESSAGES ########################
VARIABLE_IS_NOT_STR = "Variable type is not str"
VARIABLE_IS_NOT_INT = "Variable type is not int"
VARIABLE_IS_NOT_BOOL = "Variable type is not bool"

MONGOD_IS_NOT_RUNNING = "Mongodb is not running in the background"

######################## FILE TRANSFER ########################
# PATH_TO_FOLDERS_IN_PHONE = "/run/user/1000/gvfs/"
# PATH_TO_DESTINATION_IN_PC = "/home/pfm/Documents/results/"

FILES_QUANTITY_THRESHOLD = 3
