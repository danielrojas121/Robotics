from turtle import *
import sys

mode('standard')
color('orange')
speed(0)
scale = 2
offsetx = -scale/2 * 250
offsety = -scale/2 * 250

def main():
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		f = open(filename, 'r')
		read_file(f)
	done()

def read_file(infile):
	start_x, start_y = [int(x) for x in infile.readline().split()]
	goal_x, goal_y = [int(x) for x in infile.readline().split()]
	world_x, world_y = [int(x) for x in infile.readline().split()]

	draw_world(world_x, world_y)
	draw_circle(start_x, start_y)
	draw_circle(goal_x, goal_y)

	obstacle_count = int(infile.readline())
	v_count = int(infile.readline())
	line = infile.readline()
	while (line != ""):
		if v_count == 0:
			v_count = int(line)
		else:
			x, y = [float(x) for x in line.split()]
			coordinate = (x,y)
			v_count -= 1
			print coordinate
		line = infile.readline()
		
def draw_world(x, y):
	penup()
	setposition(offsetx, offsety)
	pendown()
	forward(scale * x)
	left(90)
	forward(scale * y)
	left(90)
	forward(scale * x)
	left(90)
	forward(scale * y)
	#turn left to again be in horizontal X axis
	left(90)
	penup()

def draw_circle(x, y):
	RADIUS = 3
	color('red')
	begin_fill()
	penup()
	setposition(offsetx + scale * x, offsety + scale * y)
	pendown()
	circle(RADIUS * scale)
	#turn left to again be in horizontal X axis
	penup()
	end_fill()
'''
def draw_obstacle(x, y):
	begin_fill()
	penup()
	#keep track of bottom left and top right corners of each obstacle
	bottom_left = (x-5.7, y-5.7)
	top_right = (x+5.7, y+5.7)

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
'''
main()