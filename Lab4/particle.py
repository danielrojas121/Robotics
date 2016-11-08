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

	def __repr__(self):
		return "[x=%.6s y=%.6s theta=%d]" % (str(self.x), str(self.y), self.theta)

	def set_noise(self, forward_noise, turn_noise, sense_noise):
		self.forward_noise = forward_noise
		self.turn_noise = turn_noise
		self.sense_noise = sense_noise

	def move(self, dist, theta_diff):
		if dist < 0:
			raise ValueError, "Robot can't move backwards"
		self.theta += theta_diff + random.gauss(0.0, self.turn_noise)
		self.theta %= 360
		#initialize orientation in matrix
		self.x += dist * math.cos(math.radians(self.theta))
		self.y += dist * math.sin(math.radians(self.theta))
		#wrap around when outside world boundaries
		self.x = self.x if (self.x <= self.world_x) else (self.x - self.world_x)
		self.x = self.x if (self.x >= 0.0) else (self.x + self.world_x)
		self.y = self.y if (self.y <= self.world_y) else (self.y - self.world_y)
		self.y = self.y if (self.y >= 0.0) else (self.y + self.world_y) 
		#set new particle
		copy = Particle(self.x, self.y, self.theta, 0)
		copy.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
		return copy

	def sense(self):
		dist_list = []
		for i in range(len(self.object_list)):
			dist = math.sqrt((self.x - (self.object_list[i][0] + 5.7)) ** 2 + (self.y - (self.object_list[i][1] + 5.7)) ** 2)
			dist += random.gauss(0.0, self.sense_noise)
			dist_list.append(dist)
		return dist_list

	def measurement_prob(self, measurement):
		'''calculates how likely a measurement should be'''
		prob = 1.0

		for i in range(len(self.object_list)):
			dist = math.sqrt((self.x - self.object_list[i][0])**2 + (self.y - self.object_list[i][1])**2)
			prob *= self.Gaussian(dist, self.sense_noise, measurement[i])

		return prob

	def Gaussian(self, mu, sigma, x):
		'''calculates the probability of x for 1-dim Gaussian with mean mu & var sigma'''
		sig_sq = sigma ** 2.0
		return math.exp(- ((mu-x)**2) / sig_sq / 2.0) / math.sqrt(2.0 * math.pi * sig_sq)