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
'''
	def sense(self, dist):
		dist_list = []
		theta = 0
		sense_dist = 0
		while(theta <= 180):
			theta_rad = math.radians(theta)
			delta_x =  math.cos(theta_rad) * dist
			delta_y = math.sin(theta_rad) * dist
			x = self.x + delta_x
			y = self.y + delta_y
			
		#check obstacle list to determine if sensor detects them
			for x in range(0, len(object_list)):
				obstacle = object_list[x]
		if (obstacle[0] < x) and (x < obstacle[0] + 11.4):
			if (obstacle[1] - BUFFER < y) and (y < obstacle[1] + 11.4):
				return


			#add sensor data to array and add to theta
			theta += 20
			dist_list.append(sense_dist)
		return dist_list
'''
