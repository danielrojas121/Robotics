'''Robot Class to keep track of virtual robot position'''
from particle import Particle
import random

class Robot(Particle):

    def __init__(self, x, y, theta):
        Particle.__init__(self, x, y, theta, 0)

    ''' work in progress:

    def sense(self, dist):
        dist_list = []
        theta = self.theta - 90
        sense_dist = 0
        while(theta <= self.theta + 90):
            theta_rad = math.radians(theta % 360)
            delta_x =  math.cos(theta_rad) * dist
            delta_y = math.sin(theta_rad) * dist
            sensed_x = self.x + delta_x
            sensed_y = self.y + delta_y
            #check obstacle list to determine if sensor detects them
            for i in range(0, len(object_list)):
                obstacle = object_list[i]
                if (obstacle[0] < sensed_x) and (sensed_x < obstacle[0] + 11.4):
                    if (obstacle[1] < sensed_y) and (sensed_y < obstacle[1] + 11.4):


            #add sensor data to array and add to theta
            theta += 20
            dist_list.append(sense_dist)
        return dist_list
'''