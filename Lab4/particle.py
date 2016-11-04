'''Particle Class to be used for localization'''

class Particle(object):

    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def move(self, dist, theta):
        print dist
        print theta