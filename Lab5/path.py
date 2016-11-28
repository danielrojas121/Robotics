from turtle import *
import sys

mode('standard')
color('orange')
speed(0)
scale = 2
offsetx = -scale/2 * 250
offsety = -scale/2 * 250
object_list = []
start_point = None
end_point = None
R_LENGTH = 26
R_WIDTH = 16
ORIENTATION = 0

def main():
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		f = open(filename, 'r')
		read_file(f)
		draw_objects()
		done()
	else:
		print "Error: Incorrect command line arguments"
		print "Format: python path.py <coordinates_filename>"
		sys.exit(1)

def read_file(infile):
	global start_point, end_point

	start_x, start_y = [int(x) for x in infile.readline().split()]
	goal_x, goal_y = [int(x) for x in infile.readline().split()]
	world_x, world_y = [int(x) for x in infile.readline().split()]
	start_point = (start_x, start_y)
	end_point = (goal_x, goal_y)

	draw_world(world_x, world_y)
	draw_circle(start_x, start_y)
	draw_circle(goal_x, goal_y)

	vertex_list = []

	obstacle_count = int(infile.readline())
	v_count = int(infile.readline())
	line = infile.readline()
	while (line != ""):
		if v_count == 0:
			v_count = int(line)
			object_list.append(vertex_list)
			vertex_list = []
		else:
			x, y = [float(x) for x in line.split()]
			coordinate = (x,y)
			vertex_list.append(coordinate)
			v_count -= 1
		line = infile.readline()
	object_list.append(vertex_list)

def grow_obstacles():
	global object_list, start_point, end_point

def grown_vertices(vertex):
	global R_LENGTH, R_WIDTH, ORIENTATION

	vertices = []
	theta = ORIENTATION

	return vertices

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

def draw_objects():
	global object_list

	penup()
	i = 0
	while(i<len(object_list)):
		coordinates = object_list[i]
		j = 0 
		while(j<len(coordinates)):
			setposition(coordinates[j][0] * scale + offsetx, coordinates[j][1] * scale + offsety)
			pendown()
			j+=1
		setposition(coordinates[0][0] * scale + offsetx, coordinates[0][1] * scale + offsety)
		penup()
		i+=1

main()