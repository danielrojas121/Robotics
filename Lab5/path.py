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
ORIENTATION = 45 #CANNOT BE ON THE X=0 OR Y=0 AXIS
BIG_NUMBER = 1000

def main():
	global hull_list

	if len(sys.argv) == 2:
		filename = sys.argv[1]
		f = open(filename, 'r')
		read_file(f)
		draw_objects(object_list)
		grow_obstacles()
		draw_objects(hull_list)
		graph_vertices()
		graph_edges()
		draw_edges()
		done()
	else:
		print "Error: Incorrect command line arguments"
		print "Format: python path.py <coordinates_filename>"
		sys.exit(1)

def read_file(infile):
	global start_point, end_point, ORIENTATION

	start_x, start_y = [int(x) for x in infile.readline().split()]
	goal_x, goal_y = [int(x) for x in infile.readline().split()]
	world_x, world_y = [int(x) for x in infile.readline().split()]
	start_point = (start_x, start_y)
	end_point = (goal_x, goal_y)

	delta_x = goal_x - start_x
	delta_y = goal_y - start_y

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
	#for every object compute hull points
	for obj in object_list:
		obj_verts = []
		vertices = obj
		for vertex in vertices:
			g_vertices = grown_vertices(vertex)
			for g_vertex in g_vertices:
				obj_verts.append(g_vertex)
		hull_list.append(convex_hull(obj_verts))

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
	p = lowest_point(points)
	#get points sorted in order of angularity
	points = sort_polar(points, p, n)
	#print "Sorted: ", points
	#print "-----------------------------------------------"
	#need to compute points on stack
	return find_hull(points, n)


def lowest_point(points):
	#find lowest point, if tied pick rightmost point
	p = (0, BIG_NUMBER)
	for point in points:
		if point[1] < p[1]:
			p = point
		elif point[1] == p[1]:
			if point[0] > p[0]:
				p = point   
	return p   

#sorts point based on how far they are from point 0
def sort_polar(points, p, n):
	polar_list = []
	sorted_list = []
	sorted_list.append(p)
	
	i = 0
	while(i < n):
		polar_list.append(find_polar(p, points[i], i))
		i+=1
	#secondary sort on distance away from point 0, in case of same angle
	polar_list = sorted(polar_list, key=itemgetter(1))
	#primary sort based on angular distance from point 0
	polar_list = sorted(polar_list, key=itemgetter(0))

	for p in polar_list:
		if(p[0] == 0):
			continue
		index = p[2]
		sorted_list.append(points[index])

	return sorted_list

#returns how far each point is from point 0 based on angle and distance
def find_polar(p1, p2, index):
	y = p2[1] - p1[1]
	x = p2[0] - p1[0]
	theta = math.degrees(math.atan2(y,x))
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
		if res > 0:
			stack.append(p1)
			stack.append(p2)
			stack.append(p3)
			i += 1
		elif res == 0:
			stack.append(p1)
			stack.append(p3)
			i += 1
		else:
			stack.append(p1)
	return stack

def graph_vertices():
	global hull_list, nodes, start_point, end_point
	#for every object compute hull points
	for hull in hull_list:
		del hull[-1] # LAST ELEMENT IN HULL_LIST IS A COPY OF FIRST ELEMENT
		for coordinate in hull:
			nodes.append(coordinate)
	nodes.append(start_point)
	nodes.append(end_point)

def graph_edges():
	global nodes, edges

	for i in range(0, len(nodes) - 1):
		for j in range(i+1, len(nodes)):
			edges.append((nodes[i], nodes[j]))

	valid_edges = []
	for edge in edges:
		if valid_edge(edge):
			valid_edges.append(edge)

	edges = valid_edges
	#print edges

def valid_edge(edge):
	global hull_list

	for hull in hull_list:
		#special case when edge lies within an obstacle
		if edge[0] in hull:
			v1_index = hull.index(edge[0])
			if edge[1] in hull:
				v2_index = hull.index(edge[1])
				diff = abs(v2_index - v1_index)
				if diff > 1 and diff != len(hull) - 1:
					return False

		for i in range(0, len(hull)):
			hull_p1 = hull[i]
			#special case when last and first vertex connect
			if i == len(hull) - 1:
				hull_p2 = hull[0]
			else:
				hull_p2 = hull[i+1]

			if intersect(edge[0], edge[1], hull_p1, hull_p2):
				return False

	return True

def intersect(graph_p1, graph_p2, obj_p1, obj_p2):
	'''take start and end coordinates of a graph path and object edge'''
	g_x1 = graph_p1[0]
	g_y1 = graph_p1[1]
	g_x2 = graph_p2[0]
	g_y2 = graph_p2[1]
	#line eqn: Ax + By = C
	#eqn for graph path edge
	A1 = g_y2 - g_y1
	B1 = g_x1 - g_x2
	C1 = A1*g_x1 + B1*g_y1
	#eqn for object side
	o_x1 = obj_p1[0]
	o_y1 = obj_p1[1]
	o_x2 = obj_p2[0]
	o_y2 = obj_p2[1]

	A2 = o_y2 - o_y1
	B2 = o_x1 - o_x2
	C2 = A2*o_x1 + B2*o_y1
	
	det = A1*B2 - A2*B1
	#parallel lines, won't intersect
	if(det == 0):
		return False
	else:
		#intersection point
		px = (B2*C1 - B1*C2)/det
		py = (A1*C2 - A2*C1)/det
		#check if intersection falls within path of graph edge
		if (min(g_x1, g_x2) < px) and (max(g_x1, g_x2) > px):
			if (min(g_y1, g_y2) < py) and (max(g_y1, g_y2) > py):
				#check if intersection point falls in obstacle
				if (min(o_x1, o_x2) <= px) and (max(o_x1, o_x2) >= px):
					if (min(o_y1, o_y2) <= py) and (max(o_y1, o_y2) >= py):
						return True
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
	global edges
	color('blue')
	penup()
	for edge in edges:
		setposition(edge[0][0] * scale + offsetx, edge[0][1] * scale + offsety)
		pendown()
		setposition(edge[1][0] * scale + offsetx, edge[1][1] * scale + offsety)
		penup()
	
main()