from turtle import *
import sys
import math

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
BIG_NUMBER = 1000

def main():
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		f = open(filename, 'r')
		read_file(f)
		draw_objects()
		grow_obstacles()
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
	i = 0
	object_list2 = []
	while(i<len(object_list)):
		obj_verts = []
		coordinates = object_list[i]
		j = 0 
		while(j<len(coordinates)):
			vertex_list = grown_vertices(coordinates[j])
			k = 0
			while(k<len(vertex_list)):
				obj_verts.append(vertex_list[k])
				k += 1
			j+=1
		object_list2.append(obj_verts)
		convex_hull(obj_verts)
		i+=1
	print "object_list2 ", object_list2
	print "--------------------------------------------------"
	#convex_hull(object_list2)

def grown_vertices(vertex):
	'''vertex is a coordinate tuple'''
	global R_LENGTH, R_WIDTH, ORIENTATION
	vertices = []
	theta = ORIENTATION
	x = vertex[0]
	y = vertex[1]
	vertices.append((x, y))

	x1 = x + R_LENGTH * math.cos(math.radians(theta))
	y1 = y + R_LENGTH * math.sin(math.radians(theta))
	vertices.append((x1,y1))
	theta = (theta + 90) % 360
	x2 = x1 + R_WIDTH * math.cos(math.radians(theta))
	y2 = y1 + R_WIDTH * math.sin(math.radians(theta))
	vertices.append((x2,y2))
	theta = (theta + 90) % 360
	x3 = x2 + R_LENGTH * math.cos(math.radians(theta))
	y3 = y2 + R_LENGTH * math.sin(math.radians(theta))
	vertices.append((x3,y3))
	return vertices

def convex_hull(points):
	n = len(points)
	#find rightmost, lowest points
	print "points: ", points
	print "----------------------"
	p = lowest_point(points, n)
	print "p: ", p
	print "-----------------------"
	#get points sorted in order of angularity
	points = sort_polar(points, p, n)
	print "Sorted: ", points
	print "-----------------------------------------------"


def lowest_point(points, length):
	#find lowest point, if tied pick rightmost point
	i = 0
	p = (0, BIG_NUMBER)
	while(i<length):
		if points[i][1] < p[1]:
			p = points[i]
		elif points[i][1] == p[1]:
			if points[i][0] > p[0]:
				p = points[i]	
		i+=1
	return p	

def sort_polar(points, p, n):
	i = 0
	polar_list = []
	while(i < n):
		polar_list.append(find_polar(p, points[i]))
		i+=1
	print polar_list
	#polar_list.sort(key=polar_list[0][0])
	polar_list = sorted(polar_list, key=lambda polar: polar[0])
	return polar_list


def find_polar(p1, p2):
	y = p2[1]-p1[1]
	x = p2[0] - p1[0]
	if(x == 0):
		theta = 0
		r = 0
		return (theta, r)
	theta = math.atan(y/x)
	r = math.hypot(x, y)
	return (theta, r)


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