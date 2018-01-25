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

logging.basicConfig(level=logging.INFO, format="%s(asctime)s:%(levelname)s:%s(message)s")

class ClassifyFolders:
    """
    docstring for ClassifyFolders.
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

    def classifyFile(self,
                     pathToFile):
        """
        Classify a file.
        # TODO: Complete this method with the classifier.
        Args:
            pathToFile: A string that contains the path to a file.
        Returns:
            A dictionary that contains the results of the classification.
        """
        return {"Results": None}


    def queryNotDiagnosed(self,
                          key = None,
                          value = None):
        """
        Query all the not diagnosed folders in the db.
        Args:
            key: A string that contains the key to filter.
            value: A string that contains the value to filter.
        Returns:
            A list that contains the paths of the folders that
            require to be diagnosed if that is the case. Otherwise,
            return None.
        """
        # Init local variables
        pathsNotDiagnosed = []
        if key == None:
            key = "diagnostic"
        if value == None:
            value = 0
        # Query the folder
        query = self.db.read(key = key, value = value)
        # Assert query was successful
        if query != None:
            # Create a list with the paths
            for i in query:
                pathsNotDiagnosed.append(i["path"])
            return pathsNotDiagnosed
        else:
            # There are no folders that have not been diagnosed
            return None

    @staticmethod
    def extract_images_from_folder(folder_path):
        """
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
