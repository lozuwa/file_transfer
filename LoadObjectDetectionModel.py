"""
Name: Rodrigo Loza
Email: lozuwaucb@gmail.com
Company: pfm Bolivia
Description:
"""

# Libraries
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
# Local libs
from utils import *

# Path to utils inside object localization folder
# Needs to be hardcoded.
sys.path.append(os.path.join("/home/pfm/Documents/", "models/research/object_detection/utils/"))
import label_map_util
import visualization_utils as vis_util

class LoadObjectDetectionModel(object):
	"""
	LoadObjectDetectionModel
	"""
	def __init__(self):
		super(LoadObjectDetectionModel, self).__init__()
		# Load variables
		self.PATH_TO_CKPT = os.path.join(os.getcwd(), "assets", "frozen_inference_graph.pb")
		self.PATH_TO_LABELS = os.path.join(os.getcwd(), "assets", "mscoco_label_map.pbtxt")
		self.NUM_CLASSES = 3
		self.IMAGE_SIZE = (12, 8)
		# Load graph and labels
		self.loadModel()
		self.loadLabelMap()

	def loadModel(self):
			"""
			Loads the model's frozen graph.
			"""
		self.detection_graph = tf.Graph()
		with self.detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(PATH_TO_CKPT, "rb") as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name="")

	def loadLabelMap(self):
			"""
			Loads the model's labels.
			"""
		label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
		categories = label_map_util.convert_label_map_to_categories(label_map,\
																																max_num_classes = self.NUM_CLASSES,\
																																use_display_name = True)
		self.category_index = label_map_util.create_self.category_index(categories)

	def load_image_into_numpy_array(self,
																		image):
				"""
				Converts a PILLOW image format into a numpy image format.
				Args:
						image: PILLOW format image
				Returns:
						An opencv image format.
				"""
		(im_width, im_height) = image.size
		return np.array(image.getdata()).reshape(
				(im_height, im_width, 3)).astype(np.uint8)

	def classifyFile(self,
										input_image_path = None):
				"""
				Classifies an image using the graph's model.
				Args:
						input_image_path: A string that contains the path of the image to
																classify.
				Returns:
						A boolean that indicates objects were found.
				"""
		with self.detection_graph.as_default():
			with tf.Session(graph=self.detection_graph) as sess:
				# Definite input and output Tensors for self.detection_graph
				image_tensor = detection_g	raph.get_tensor_by_name("image_tensor:0")
				# Each box represents a part of the image where a particular object was detected.
				detection_boxes = self.detection_graph.get_tensor_by_name("detection_boxes:0")
				# Each score represent how level of confidence for each of the objects.
				# Score is shown on the result image, together with the class label.
				detection_scores = self.detection_graph.get_tensor_by_name("detection_scores:0")
				detection_classes = self.detection_graph.get_tensor_by_name("detection_classes:0")
				num_detections = self.detection_graph.get_tensor_by_name("num_detections:0")

				# Actual classification
				image = Image.open(input_image_path)
				# the array based representation of the image will be used later in order to prepare the
				# result image with boxes and labels on it.
				image_np = self.load_image_into_numpy_array(image)
				# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
				image_np_expanded = np.expand_dims(image_np, axis = 0)
				# Actual detection.
				(boxes, scores, classes, num) = sess.run(
						[detection_boxes, detection_scores, detection_classes, num_detections],
						feed_dict={image_tensor: image_np_expanded})
				# Visualization of the results of a detection.
				vis_util.visualize_boxes_and_labels_on_image_array(image_np,
																											np.squeeze(boxes),
																											np.squeeze(classes).astype(np.int32),
																											np.squeeze(scores),
																											self.category_index,
																											use_normalized_coordinates=True,
																											line_thickness=8)
				if max(np.squeeze(scores)) > 0.80:
					# @DEPRECATED
					# image = Image.fromarray(image_np)
					# image.save(output_image_path)
					return True, (np.squeeze(classes), np.squeeze(scores), image_np)
				else:
					return False, None
				# plt.figure(figsize=self.IMAGE_SIZE)
				# plt.imshow(image_np)
