'''Robot Class to keep track of virtual robot position'''
from particle import Particle

class Robot(Particle):

    def __init__(self, x, y, theta):
        Particle.__init__(self, x, y, theta, 0)