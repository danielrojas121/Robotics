import sys
import random
import numpy as np
import math
import time
from turtle import *
from particle import Particle
from robot import Robot

mode('standard')
color('orange')
speed(0)
scale = 3
offsetx = -scale/2 * 150
offsety = -scale/2 * 150
particle_count = 0
world_x = 0
world_y = 0
object_list = [] #store position of map objects in this list
particle_list = [] #store Particle instances in this list
robot = None
robotGuess = None
updates = 0
MOVES = 10
BUFFER = 1 #maintain particles a certain distance from objects

def main():
	global particle_list, robotGuess, updates

	MIN_DIST = 5.0
	MAX_DIST = 20.0
	SENSE_DIST = MAX_DIST + MIN_DIST

	if len(sys.argv) == 3:
		createInitialObjects()
		createInitialParticles()
		createInitialRobot()
		stampAll()
	else:
		print "Error: Incorrect command line arguments"
		print "Format: python locate.py <coordinates_filename> <particle_count>"
		sys.exit(1)
	
	print "Mean error at start", meanError(robot, particle_list)
	#print particle_list

	for move in range(MOVES):
		dist = random.random() * MAX_DIST + MIN_DIST
		theta_diff = 0

		while (not robot.validMove(dist, robot.theta)):
			dist = random.random() * MAX_DIST + MIN_DIST
			robot.move(0, 45)
			theta_diff += 45
		
		robot.move(dist, 0)
		updates += 1
		r_dist_list = robot.sense(SENSE_DIST)

		p2 = []
		for i in range(particle_count):
			p2.append(particle_list[i].move(dist, theta_diff))

		particle_list = p2

		weight_list = []
		for i in range(particle_count):
			p = particle_list[i]
			p_dist_list = p.sense(SENSE_DIST)
			weight_list.append(p.measurement_prob(r_dist_list, p_dist_list))

		p3 = []
		index = int(random.random() * particle_count)
		beta = 0.0
		max_weight = max(weight_list)
		for i in range(particle_count):
			beta += random.random() * 2.0 * max_weight
			while beta > weight_list[index]:
				beta -= weight_list[index]
				index = (index + 1) % particle_count
			p3.append(particle_list[index])

		particle_list = p3
		robotGuess = meanLocation(particle_list)
		updates += 1

		if move % 5 == 0:
			stampAll()

	print "Total updates:", updates
	print "Mean location", meanLocation(particle_list)
	print "Mean error", meanError(robot, particle_list)

	stampAll()

	print ' '
	if meanError(robot, particle_list) > 0.0:
		for i in range(particle_count/100):
			print 'Final particle #', i*100, particle_list[i*100]
		print ' '
		print 'Actual Robot Location', robot
	
	done()

def createInitialObjects():
	global world_x, world_y, object_list
	filename = sys.argv[1]
	with open(filename, 'r') as f:
		world_x, world_y = [int(x) for x in next(f).split()]
		drawWorld(world_x, world_y)
		for line in f:
			x, y = [float(x) for x in line.split()]
			if x-5.7 >= 0 and x+5.7 <= world_x and y-5.7 >= 0 and y+5.7 <= world_y:
				drawObstacle(x, y)
			else:
				print "Obstacle at %d, %d is outside the world bounds" % (x,y)
				sys.exit(1)
	#Initialize Particle class static variables
	Particle.world_x = world_x
	Particle.world_y = world_y
	Particle.object_list = object_list

def createInitialParticles():
	global particle_count, robotGuess
	particle_count = int(sys.argv[2])
	for p in range(0, particle_count):
		positionTuple = findRandomPosition()
		i = positionTuple[0]
		j = positionTuple[1]
		theta = positionTuple[2]
		
		#add particle to particle_list
		particle = Particle(i, j, theta, 0)
		particle.set_noise(0.05, 0.05, 5.0)
		particle_list.append(particle)
	robotGuess = meanLocation(particle_list)

def createInitialRobot():
	global robot
	positionTuple = findRandomPosition()
	i = positionTuple[0]
	j = positionTuple[1]
	theta = positionTuple[2]
	robot = Robot(i, j, theta)

def findRandomPosition():
	global world_x, world_y

	i = random.random() * world_x
	j = random.random() * world_y
	theta = random.randint(0, 359)

	while occupiedLocation(i,j):
		i = random.random() * world_x
		j = random.random() * world_y

	return (i, j, theta)	

def occupiedLocation(x, y):
	for i in range(0, len(object_list)):
		obstacle = object_list[i]
		if (obstacle[0] - BUFFER < x) and (x < obstacle[0] + 11.4 + BUFFER):
			if (obstacle[1] - BUFFER < y) and (y < obstacle[1] + 11.4 + BUFFER):
				return True
	return False

def drawWorld(x, y):
	penup()
	setposition(offsetx, offsety)
	pendown()
	forward(scale*x)
	left(90)
	forward(scale*y)
	left(90)
	forward(scale*x)
	left(90)
	forward(scale*y)
	#turn left to again be in horizontal X axis
	left(90)
	penup()

def drawObstacle(x, y):
	begin_fill()
	penup()
	#keep track of bottom left and top right corners of each obstacle
	bottom_left = (x-5.7, y-5.7)
	top_right = (x+5.7, y+5.7)
	
	object_list.append(bottom_left)

	setposition(offsetx + scale*bottom_left[0], offsety + scale*bottom_left[1])
	pendown()
	forward(scale*11.4)
	left(90)
	forward(scale*11.4)
	left(90)
	forward(scale*11.4)
	left(90)
	forward(scale*11.4)
	#turn left to again be in horizontal X axis
	left(90)
	penup()
	end_fill()

def stampAll():
	global robot, particle_list, robotGuess
	clearstamps()
	stampRobot(robot, 'red')
	for i in range(0, len(particle_list)):
		p = particle_list[i]
		#draw every 10 particles
		if i % 10 == 0:
			stampParticle(p)
	stampRobot(robotGuess, 'gray')
	time.sleep(1)

def stampParticle(particle):
	x = particle.x
	y = particle.y
	theta = particle.theta
	color('blue')
	shape('circle')
	resizemode('user')
	turtlesize(.07,.07,.1)
	setheading(theta)
	setposition(offsetx + scale*x, offsety + scale*y)
	stamp()

def stampRobot(robot, _color):
	x = robot.x
	y = robot.y
	theta = robot.theta
	color(_color)
	shape('circle')
	resizemode('user')
	turtlesize(1.0,1.0,2.0)
	setheading(theta)
	setposition(offsetx + scale*x, offsety + scale*y)
	stamp()

def meanError(robot, particles):
	sum = 0.0
	for i in range(len(particles)):
		dx = (particles[i].x - robot.x + (world_x/2.0)) % world_x - (world_x/2.0)
		dy = (particles[i].y - robot.y + (world_y/2.0)) % world_y - (world_y/2.0)
		err = sqrt(dx * dx + dy * dy)
		sum += err
	return sum / float(len(particles))

def meanLocation(particles):
	count = len(particles)
	x_sum = 0.0
	y_sum = 0.0
	theta_sum = 0
	
	for i in range(count):
		p = particles[i]
		x_sum += p.x
		y_sum += p.y
		theta_sum += p.theta

	x_avg = x_sum / float(count)
	y_avg = y_sum / float(count)
	theta_avg = theta_sum / float(count)
	return Robot(x_avg, y_avg, theta_avg)

main()