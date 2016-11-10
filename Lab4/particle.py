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


	def intersect(self, theta, p1, p2, dist):
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
    		return 0
    	else:
    		#intersection point
    		px = (B2*C1 - B1*C2)/det
    		py = (A1*C2 - A2*C1)/det
    		#check if intersection point falls in obstacle
			if (min(p1[0], p2[0]) < px) and (max(p1[0], p2[0]) > px):
		    	if (min(p1[1], p2[1]) < py) and (max(p1[1], p2[1]) > py):
		    		dist = sqrt((px - self.x)**2 + (py - self.y)**2)
		    		return dist
        	return 0

        
    def sense(self, dist):
        dist_list = []
    	theta = self.theta - 90
    	sense_dist = 0
    	while(theta <= self.theta + 90):
    		#check obstacle list to determine if sensor detects them at this angle theta
    		intersects_list = []
    		for i in range(0, len(object_list)):
    			obstacle = object_list[i]
    			p1 = (obstace[0], obstacle[1]) 
    			p2 = (obstacle[0]+11.4, obstacle[1])
    			p3 = (obstacle[0], obstacle[1]+11.4) 
    			p4 = (obstace[0]+11.4, obstacle[1]+11.4)
    			#also need points for the wall 
    			intersects = [intersect(theta, p1, p2, dist), intersect(theta, p1, p3, dist), 
    				intersect(theta, p3, p4, dist), intersect(theta, p2, p4, dist)]
    			#add intersections from this obstacle to overall list of intersections
    			intersects_list.extend(intersects)
    			
    		#find closest intersection out of all the obstacles
    		min_dist = dist*2 
			for j in range(0, len(intersects_list)):
				if intersects_list[j] < min_dist and intersects_list[j] != 0:
					min_dist = intersects_list[j]
			#if no intersection at this theta then add 0 to list
			#a real sensor should never return a distance of 0
        	#since that would mean it's in an object
        	#so 0 is a safe number to use to indicate no objects nearby
			if min_dist == dist*2:
				min_dist = 0
        	#add sensor data to array
        	dist_list.append(min_dist)
        	#add to theta to continue sensing
        	theta += 20
    	return dist_list
