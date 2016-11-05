'''Particle Class to be used for localization'''
import numpy as np
import math

class Particle(object):
    position_matrix = np.matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
    translation_matrix = np.matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
    
    def __init__(self, x, y, theta, weight):
        self.x = x
        self.y = y
        self.theta = theta
        self.weight = weight
        #initialize coordinates in matrix
        self.position_matrix[0,2] = x
        self.position_matrix[1,2] = y

    def move(self, dist, theta_diff):
        self.theta += theta_diff
        #initialize orientation in matrix
        self.translation_matrix[0,2] = dist * math.cos(math.radians(self.theta))
        self.translation_matrix[1,2] = dist * math.sin(math.radians(self.theta))

        self.position_matrix = np.dot(self.translation_matrix, self.position_matrix)

        self.x = self.position_matrix[0,2]
        self.y = self.position_matrix[1,2]
        return (self.x, self.y, self.theta)

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
		        



            #add sensor data to array and add to theta
            theta += 20
            dist_list.append(sense_dist)
        return dist_list
