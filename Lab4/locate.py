import sys
import random
import numpy as np
import math
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
object_list = [] #store position of map objects in this list
particle_list = [] #store Particle instances in this list
world_x = 0
world_y = 0
BUFFER = 1 #maintain particles a certain distance from objects

def main():
	if len(sys.argv) == 3:
		drawInitialObjects()
		drawParticles()
		done()
	else:
		print "Error: Incorrect command line arguments"
		print "Format: python locate.py <coordinates_filename> <particle_count>"
		sys.exit(1)

def drawInitialObjects():
	global object_list, particle_count, particle_list, world_x, world_y
	filename = sys.argv[1]
	with open(filename, 'r') as f:
		world_x, world_y = [int(x) for x in next(f).split()]
		drawWorld(world_x, world_y)
		for line in f:
			x, y = [float(x) for x in line.split()]
			drawObstacle(x, y)

def drawParticles():
	global world_x, world_y
	clearstamps()
	particle_count = int(sys.argv[2])
	for p in range(0, particle_count):
		positionTuple = findRandomPosition()
		i = positionTuple[0]
		j = positionTuple[1]
		theta = positionTuple[2]
		
		#add particle to particle_list
		particle = Particle(i, j, theta, 0)
		particle_list.append(particle)
		#draw every 10 particles
		if p % 10 == 0:
			stampParticle(i, j, theta)
	
	positionTuple = findRandomPosition()
	i = positionTuple[0]
	j = positionTuple[1]
	theta = positionTuple[2]
	robot = Robot(i, j, theta)
	stampRobot(i, j, theta)

def findRandomPosition():
	global world_x, world_y

	i = random.random() * world_x
	j = random.random() * world_y
	theta = random.randint(0, 359)
	restart = True
	while restart:
		restart = False
		for x in range(0, len(object_list)):
			obstacle = object_list[x]
			if (obstacle[0] - BUFFER < i) and (i < obstacle[0] + 11.4 + BUFFER):
				if (obstacle[1] - BUFFER < j) and (j < obstacle[1] + 11.4 + BUFFER):
					i = random.random() * world_x
					j = random.random() * world_y
					restart = True
					break
	return (i, j, theta)	

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
	global object_list
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

def stampParticle(x, y, theta):
	color('blue')
	shape('circle')
	resizemode('user')
	turtlesize(.07,.07,.1)
	setheading(theta)
	setposition(offsetx + scale*x, offsety + scale*y)
	stamp()

def stampRobot(x, y, theta):
	color('red')
	shape('circle')
	resizemode('user')
	turtlesize(1.0,1.0,2.0)
	setheading(theta)
	setposition(offsetx + scale*x, offsety + scale*y)
	stamp()

main()