'''Robot Class to keep track of virtual robot position'''
from particle import Particle
import random

class Robot(Particle):

    def __init__(self, x, y, theta):
        Particle.__init__(self, x, y, theta, 0)
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0