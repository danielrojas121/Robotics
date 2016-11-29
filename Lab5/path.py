from turtle import *
from operator import itemgetter
from matplotlib import path
import matplotlib.pyplot as plt
import sys
import math

mode('standard')
color('orange')
speed(0)
scale = 2
offsetx = -scale/2 * 250
offsety = -scale/2 * 250
object_list = []
hull_list = []
nodes = []
edges = []
start_point = None
end_point = None
R_LENGTH = 26
R_WIDTH = 16
ORIENTATION = 45
BIG_NUMBER = 1000

def main():
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		f = open(filename, 'r')
		read_file(f)
		draw_objects(object_list)
		grow_obstacles()
		draw_objects(hull_list)
		graph_vertices()
		graph_edges()
		#draw_edges()

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
	global object_list, hull_list
	i = 0
	#for every object compute hull points
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
		hull_list.append(convex_hull(obj_verts))
		i+=1


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
	p = lowest_point(points, n)
	#get points sorted in order of angularity
	points = sort_polar(points, p, n)
	print "Sorted: ", points
	print "-----------------------------------------------"
	#need to compute points on stack
	return find_hull(points, n)


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

#sorts point based on how far they are from point 0
def sort_polar(points, p, n):
	i = 0
	polar_list = []
	sorted_list = []
	sorted_list.append(p)
	while(i < n):
		polar_list.append(find_polar(p, points[i], i))
		i+=1
	#secondary sort on distance away from point 0, in case of same angle
	polar_list = sorted(polar_list, key=itemgetter(1))
	#primary sort based on angular distance from point 0
	polar_list = sorted(polar_list, key=itemgetter(0))
	i = 0
	while(i<n):
		if(polar_list[i][0] == 0):
			i+=1
			continue
		index = polar_list[i][2]
		sorted_list.append(points[index])
		i+=1
	return sorted_list


#returns how far each point is from point 0 based on angle and distance
def find_polar(p1, p2, index):
	y = p2[1] - p1[1]
	x = p2[0] - p1[0]
	if(x == 0):
		if y==0: 
			theta = 0
		else: 
			theta = 90
		r = y
		return (theta, r, index)
	theta = math.degrees(math.atan(y/x))
	if theta < 0 or theta == -0.0: 
		theta = 180 + theta
	r = math.hypot(x, y)
	return (theta, r, index)

def find_hull(points, n):
	stack = []
	stack.append(points[n-1])
	stack.append(points[0])

	i = 1
	while (i < n):
		p2 = stack.pop()
		p1 = stack.pop()
		p3 = points[i]
		
		res = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
		if res >= 0:
			stack.append(p1)
			stack.append(p2)
			stack.append(p3)
			i += 1
		else:
			stack.append(p1)
	return stack

def graph_vertices():
	global hull_list, nodes, start_point, end_point
	i = 0
	#for every object compute hull points
	while(i<len(hull_list)):
		coordinates = hull_list[i]
		j = 0 
		while(j<len(coordinates)):
			nodes.append(coordinates[j])
			j+=1
		i+=1
	nodes.append(start_point)
	nodes.append(end_point)

def graph_edges():
	global nodes

	#p = path.Path(nodes)
	#print p
	#print p.contains_points([(5,5), (4,0), (6,0), (10,5), (5,10), (0,5)], radius=0.01)
	i = 0
	while(i<len(nodes))


def intersect(p1, p2, p3, p4):
	'''intersects stuff'''
	x2 = p2[0]
	x1 = p1[0]
	y2 = p2[1]
	y1 = p1[1]
	#line eqn: Ax + By = C
	#eqn for edge
	A1 = y2 - y1
	B1 = x1 - x2
	C1 = A1*x1 + B1*y1
	#eqn for object side line 
	A2 = p4[1] - p3[1]
	B2 = p3[0] - p4[0]
	C2 = A2*p3[0] + B2*p3[1]
	det = A1*B2 - A2*B1
	#parallel lines, won't intersect
	if(det == 0):
		return None
	else:
		#intersection point
		px = (B2*C1 - B1*C2)/det
		py = (A1*C2 - A2*C1)/det
		#check if intersection falls on path of movement
		if (min(x1, x2) < px) and (max(x1, x2) > px):
			if (min(y1, y2) < py) and (max(y1, y2) > py):
				#check if intersection point falls in obstacle
				if (min(p1[0], p2[0]) < px) and (max(p1[0], p2[0]) > px):
					if (min(p1[1], p2[1]) < py) and (max(p1[1], p2[1]) > py):
						#dist = math.sqrt((px - x1)**2 + (py - y1)**2)
						return True
		#if no intersection just return None
		return False

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

def draw_objects(object_list):
	#global object_list
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

def draw_edges():
	global nodes, edges, object_list
	penup()
	for i in range(0, len(nodes) - 1):
		for j in range(i+1, len(nodes)):
			for k in range(0, len(object_list)):
				coordinates = object_list[k]
				for m in range(0, len(coordinates)):
					if intersects: 

			setposition(nodes[i][0] * scale + offsetx, nodes[i][1] * scale + offsety)
			pendown()
			setposition(nodes[j][0] * scale + offsetx, nodes[j][1] * scale + offsety)
			penup()

			j += 1
		i += 1

main()