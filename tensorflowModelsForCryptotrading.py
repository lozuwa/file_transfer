# Libraries
import os
import sys
import tensorflow as tf
import numpy as np

class VanillaNeuralNetwork(object):
	"""
	Simple neural network model. 
	See __repr__ to instantiate the class.
	"""
	def __repr__(self):
		return "VanillaNeuralNetwork({}, {}, {}, {})".format("3", 
						"[3,6,1]", "0.001", "1000")

	def __init__(self,
								x = None,
								y = None,
								layers = None,
								neurons = None,
								learningRate = None,
								epochs = None):
		super(VanillaNeuralNetwork, self).__init__()
		# Init null objects
		if layers == None:
			raise Exception("layers cannot be empty.")
		if neurons == None:
			raise Exception("neurons canot be empty.")
		if learningRate == None:
			learningRate = 0.001
		if epochs == None:
			epochs = 1000
		if x == None:
			raise Exception("x is the input data, provide it.")
		if y == None:
			raise Exception("y is the input data, provide it.")
		# Assertions
		if len(neurons) != layers:
			raise ValueError("layers and len(neurons) must be equal.")
		# Class variables
		self.layers = layers
		self.neurons = neurons
		self.learningRate = learningRate
		self.epochs = epochs
		self.x = x
		self.y = y
		self.xInput = tf.placeholder(tf.float32, [1, 1])
		self.yInput = tf.placeholder(tf.float32, [1, 1])
		# Init weights
		self.initWeights()

	def initWeights(self):
		# Create a hash map to store the weights and bias
		self.weights = {}
		self.bias = {}
		# Create weight and bias matrices
		for i in range(self.layers-1):
			# Get the amount of neurons
			currentNeurons = self.neurons[i]
			nextNeurons = self.neurons[i+1]
			# Weights (axb)
			self.weights["w_{}_{}".format(i, i+1)] 
				= tf.Variable(tf.random_normal(currentNeurons, nextNeurons))
			# Bias (1xb)
			self.bias["b_{}_{}".format(i, i+1)]
				= tf.Variable(tf.random_normal(nextNeurons))

	def logits(self,
						inputValue):
		# Compute first layer
		prevLayer = tf.add(tf.matmul(inputValue, self.weights["w_0_1"]),
												self.bias["b_0_1"])
		# Basis function (relu)
		prevLayer = tf.maximum(prevLayer, 0)
		# Compute the rest of the forward prop
		for i in range(1, self.layers-1):
			nextLayer = tf.add(tf.matmul(prevLayer,
												self.weights["w_{}_{}".format(i, i+1)]),
												self.bias["b_{}_{}"])
			# Basis function (relu)
			nextLayer = tf.maximum(nextLayer, 0)
			prevLayer = nextLayer
		return nextLayer

	def train(self):
		# Logits
		logits = self.logits(self.xInput)
		# Cost function (MSE)
		lossFunction = tf.reduce_mean(tf.pow(logits - self.yInput), 2)
		# Optimizer
		optimizer = tf.train.RMSPropOptimizer(learning_rate = 
																								self.learningRate).
																								minimize(lossFunction)
		# Initializer
		init = tf.global_variables_initializer()
		# TF Session
		with tf.Session() as sess:
			sess.run(init)
			for epoch in range(self.epochs):
				# Run the training operation
				avg_cost = 0
				for i in range(self.x.shape[1]):
					x_val_for_placeholder = np.array(self.x[0, i]).reshape(1, 1)
					y_val_for_placeholder = np.array(self.y[0, i]).reshape(1, 1)
					_, cost = sess.run([optimizer, lossFunction], 
															feed_dict={self.xInput: x_val_for_placeholder,
																			 self.yInput: y_val_for_placeholder})
					avg_cost += cost
				# Feedback
				if epoch % 10 == 0:
					print("Iteration {} :: cost: {}".format(epoch, avg_cost / self.x.shape[1]))

			print("\nTraining finished, check accuracy ...")
			predictions = []
			for i in range(self.x.shape[1]):
				output = sess.run(self.logits(self.xInput), 
													feed_dict={self.xInput: np.array(self.x[0, i]).reshape(1, 1)})
				predictions.append(np.squeeze(output))
			print(predictions)
			plt.scatter(self.x[0,:], predictions)
			plt.title("Predicted curve")
			plt.show()

