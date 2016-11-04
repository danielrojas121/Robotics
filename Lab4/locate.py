import sys
import random
import numpy as np
import math
from turtle import *

mode('standard')
color('red')
speed(0)
scale = 3
offsetx = -scale/2 * 150
offsety = -scale/2 * 150
particle_count = 0
object_list = []
particle_list = []
matrix = None

def main():
	if len(sys.argv) == 3:
		drawInitialObjects()
	else:
		print "Error: Incorrect command line arguments"
		print "Format: python particle.py <coordinates_filename> <particle_count>"
		sys.exit(1)

def drawInitialObjects():
	global object_list, particle_count, matrix
	filename = sys.argv[1]
	with open(filename, 'r') as f:
		world_x, world_y = [int(x) for x in next(f).split()]
		matrix = np.empty(shape=(world_y, world_x))
		matrix.fill(-1) #-1 for any 'empty' space
		drawWorld(world_x, world_y)
		for line in f:
			x, y = [float(x) for x in line.split()]
			drawObstacle(x, y)
	particle_count = int(sys.argv[2])
	for p in range(0, particle_count):
		i = random.randint(0, world_x)
		j = random.randint(0, world_y)
		theta = random.randint(0, 359)
		'''for x in range(0, len(object_list)):
			obstacle = object_list[x]
			if (obstacle[0] < i) AND (i < obstacle[0] + 11.4) AND (obstacle[1] < j) AND (j < obstacle[1] + 11.4):
				i = random.randint(0, world_x)
				j = random.randint(0, world_y)
'''
		#iterate through obstacles to make sure particle position ok
		#if ok, add to particle list here (remove from draw particle)
		#if p%10==0 draw particle
	#mark matrix with each particle
	matrix[0,0] = 1
	drawParticle(0,0,0)
	print matrix
	print object_list
	print particle_list
	done()

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
	global object_list, matrix
	begin_fill()
	penup()
	#keep track of bottom left and top right corners of each obstacle
	bottom_left = (x-5.7, y-5.7)
	top_right = (x+5.7, y+5.7)
	
	object_list.append(bottom_left)
	#mark objects in matrix
	#ceil & floor to get actual integer indexes for matrix
	for x in range(int(math.ceil(bottom_left[0])), int(math.floor(top_right[0])+1)):
		for y in range(int(math.ceil(bottom_left[1])), int(math.floor(top_right[1])+1)):
			matrix[x,y] = 0

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

def drawParticle(x, y, theta):
	global particle_list
	color('blue')
	begin_fill()
	penup()
	particle = [x, y, theta] #move this and...
	particle_list.append(particle) #move this outside to include ALL particles
	setposition(offsetx + scale*x, offsety + scale*y)
	pendown()
	circle(1)
	penup()
	end_fill()

main()