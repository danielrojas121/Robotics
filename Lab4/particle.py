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
		#
		self.theta += theta_diff + random.gauss(0.0, self.turn_noise)
		self.theta %= 360
		#initialize orientation in matrix
		self.x += dist * math.cos(math.radians(self.theta))
		self.y += dist * math.sin(math.radians(self.theta))
		#set new particle
		copy = Particle(self.x, self.y, self.theta, 0)
		copy.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
		return copy

	def validMove(self, dist, theta):
		new_x = self.x + dist * math.cos(math.radians(theta))
		new_y = self.y + dist * math.sin(math.radians(theta))

		if not self.inWorld(new_x, new_y):
			return False

		for intersect in self.intersections(dist, theta):
			if intersect != None:
				return False

		return True

	def inWorld(self, x, y):
		if x < 0 or x > self.world_x or y < 0 or y > self.world_y:
			return False
		return True
	'''
	def sense(self):
		dist_list = []
		for i in range(len(self.object_list)):
			dist = math.sqrt((self.x - (self.object_list[i][0] + 5.7)) ** 2 + (self.y - (self.object_list[i][1] + 5.7)) ** 2)
			dist += random.gauss(0.0, self.sense_noise)
			dist_list.append(dist)
		return dist_list
	'''
	def measurement_prob(self, robot_sense, particle_sense):
		'''calculates how likely a measurement should be'''
		prob = 1.0
		print "robot sense:", robot_sense
		print "particle sense:", particle_sense
		if not self.inWorld(self.x, self.y): 
			return 0.0

		for i in range(len(particle_sense)):
			dist = particle_sense[i]
			prob *= self.Gaussian(dist, self.sense_noise, robot_sense[i])

		return prob

	def Gaussian(self, mu, sigma, x):
		'''calculates the probability of x for 1-dim Gaussian with mean mu & var sigma'''
		sig_sq = sigma ** 2.0
		return math.exp(- ((mu-x)**2) / sig_sq / 2.0) / math.sqrt(2.0 * math.pi * sig_sq)


	def intersect(self, theta, p1, p2, dist):
		'''intersects stuff'''
		theta_rad = math.radians(theta % 360)
		delta_x =  math.cos(theta_rad) * dist
		delta_y = math.sin(theta_rad) * dist
		x2 = self.x + delta_x
		y2 = self.y + delta_y
		#line eqn: Ax + By = C
		#eqn for sense line from particle out
		A1 = y2 - self.y
		B1 = self.x - x2
		C1 = A1*self.x + B1*self.y
		#eqn for obstacle side line 
		A2 = p2[1] - p1[1]
		B2 = p1[0] - p2[0]
		C2 = A2*p1[0] + B2*p1[1]
		det = A1*B2 - A2*B1
		#parallel lines, won't intersect
		if(det == 0):
			return None
		else:
			#intersection point
			px = (B2*C1 - B1*C2)/det
			py = (A1*C2 - A2*C1)/det
			#check if intersection point falls in obstacle
			if (min(p1[0], p2[0]) <= px) and (max(p1[0], p2[0]) >= px):
				if (min(p1[1], p2[1]) <= py) and (max(p1[1], p2[1]) >= py):
					dist = math.sqrt((px - self.x)**2 + (py - self.y)**2)
					return dist
			#if no intersection just return None
			return None

	def intersections(self, dist, theta): 
		intersects = []
		for i in range(0, len(self.object_list)):
			obstacle = self.object_list[i]
			p1 = (obstacle[0], obstacle[1]) # bottom left
			p2 = (obstacle[0]+11.4, obstacle[1]) # bottom right
			p3 = (obstacle[0], obstacle[1]+11.4) # top left
			p4 = (obstacle[0]+11.4, obstacle[1]+11.4) # top right
			#also need points for the wall
			intersects.append(self.intersect(theta, p1, p2, dist)) 
			intersects.append(self.intersect(theta, p1, p3, dist)) 
			intersects.append(self.intersect(theta, p3, p4, dist))
			intersects.append(self.intersect(theta, p2, p4, dist))
		#corner points for world walls
		w1 = (0.0, 0.0) # bottom left
		w2 = (self.world_x, 0.0) # bottom right
		w3 = (0.0, self.world_y) # top left
		w4 = (self.world_x, self.world_y) # top right
		intersects.append(self.intersect(theta, w1, w2, dist))
		intersects.append(self.intersect(theta, w1, w3, dist))
		intersects.append(self.intersect(theta, w3, w4, dist))
		intersects.append(self.intersect(theta, w2, w4, dist))
		return intersects

	def sense(self, dist):
		dist_list = []
		theta = self.theta - 90
		intersects_list = []
		while(theta <= self.theta + 90):
			#check obstacle list and walls to determine if sensor detects them at this angle theta
			intersects_list = self.intersections(dist, theta)
				
			#find closest intersection out of all the obstacles
			min_dist = self.world_x * self.world_y 
			for j in range(0, len(intersects_list)):
				if intersects_list[j] < min_dist and intersects_list[j] != None:
					min_dist = intersects_list[j]

			#add sensor data to array
			dist_list.append(min_dist)
			#add to theta to continue sensing
			theta += 20
		return dist_list
