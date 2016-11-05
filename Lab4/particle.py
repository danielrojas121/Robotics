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
