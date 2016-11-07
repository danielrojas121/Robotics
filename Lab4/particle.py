'''Particle Class to be used for localization'''
import numpy as np
import random
import math

class Particle(object):
	world_x = 0.0
	world_y = 0.0
	object_list = []

	def __init__(self, x, y, theta, weight):
		self.x = x
		self.y = y
		self.theta = theta
		self.weight = weight
		self.forward_noise = 0.0
		self.turn_noise = 0.0
		self.sense_noise = 0.0

	def __str__(self):
		'''This function allows for pretty printing of Particle objects'''
		return "(%f, %f, %d)" % (self.x, self.y, self.theta)

	def move(self, dist, theta_diff):
		if dist < 0:
			raise ValueError, "Robot can't move backwards"
		self.theta += theta_diff + random.gauss(0.0, self.turn_noise)
		self.theta %= 360
		#initialize orientation in matrix
		self.x += dist * math.cos(math.radians(self.theta))
		self.y += dist * math.sin(math.radians(self.theta))
		#wrap around
		self.x = self.x if (self.x <= self.world_x) else (self.x - self.world_x)
		self.y = self.y if (self.y <= self.world_y) else (self.y - self.world_y) 
		#set new particle
		copy = Particle(self.x, self.y, self.theta, 0)
		return copy

	def sense(self):
		dist_list = []
		for i in range(len(self.object_list)):
			dist = math.sqrt((self.x - (self.object_list[i][0] + 5.7)) ** 2 + (self.y - (self.object_list[i][1] + 5.7)) ** 2)
			dist += random.gauss(0.0, self.sense_noise)
			dist_list.append(dist)
		return dist_list