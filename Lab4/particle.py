import sys
from turtle import *

mode('standard')
color('red')
speed(0)

def main():
	if len(sys.argv) == 2:
		readFile()
	else:
		print "Error: Must provide one coordinate text file as an argument"
		sys.exit(1)


def readFile():
	with open(sys.argv[1], 'r') as f:
		world_x, world_y = [int(x) for x in next(f).split()]
		drawWorld(world_x, world_y)
		for line in f:
			x, y = [float(x) for x in line.split()]
			drawObstable(x, y)
	done()

def drawWorld(x, y):
	penup()
	setposition(0,0)
	pendown()
	forward(x)
	left(90)
	forward(y)
	left(90)
	forward(x)
	left(90)
	forward(y)
	#turn left to again be in horizontal X axis
	left(90)
	penup()

def drawObstable(x, y):
	penup()
	setposition(x - 5.7, y - 5.7)
	pendown()
	forward(11.4)
	left(90)
	forward(11.4)
	left(90)
	forward(11.4)
	left(90)
	forward(11.4)
	#turn left to again be in horizontal X axis
	left(90)
	penup()

main()