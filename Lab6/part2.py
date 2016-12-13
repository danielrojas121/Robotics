from turtle import *
import random
import matplotlib.pyplot as plt
import sys
import math

mode('standard')
color('orange')
speed(0)
scale = 1
offsetx = -scale/2 * 300
offsety = -scale/2 * 300
WORLD_X = 600
WORLD_Y = 600
object_list = []
STEP_SIZE = 25
N = 3000
connected = False

def main():

    if len(sys.argv) == 3:
        filename = sys.argv[1]
        obj_file = open(filename, 'r')
        filename = sys.argv[2]
        goal_file = open(filename, 'r')
        read_obj_file(obj_file)
        start_point, end_point = read_goal_file(goal_file)
        tree1, tree2 = build_rrt(start_point, N, end_point) #tree is a tuple of nodes & edges
        draw_world(WORLD_X, WORLD_Y)
        draw_objects(object_list)
        draw_circle(start_point[0], start_point[1])
        draw_circle(end_point[0], end_point[1])
        color('blue')
        draw_edges(tree1[1])
        color('red')
        draw_edges(tree2[1])
        if connected:
            tree = join_trees(tree1, tree2)
            nodes_dict = build_dict(tree)
            path = find_path(start_point, end_point, tree[0], nodes_dict)
            draw_path(path[0])
        done()
    else:
        print "Error: Incorrect command line arguments"
        print "Format: python part2.py <obstacle_filename> <goal_filename>"
        sys.exit(1)

def read_obj_file(infile):
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

def read_goal_file(infile):
    start_x, start_y = [int(x) for x in infile.readline().split()]
    goal_x, goal_y = [int(x) for x in infile.readline().split()]
    start_point = (start_x, start_y)
    end_point = (goal_x, goal_y)
    return start_point, end_point

def build_rrt(q_0, n, end_point):
    global connected
    nodes = []
    edges = []
    nodes2 = []
    edges2 = []
    tree1 = True;

    nodes.append(q_0)
    nodes2.append(end_point)
    for i in range(n):
        x_rand = random.randint(0, WORLD_X)
        y_rand = random.randint(0, WORLD_Y)
        q_rand = (x_rand, y_rand)
        
        if(tree1):
            edge = extend_rrt(nodes, edges, q_rand)
            if edge != None:
                nodes.append(edge[1]) #the second node is the new node
                edges.append(edge)
                tree1 = not tree1
                if edge[1] == nodes2[-1]:
                    connected = True
                    break
                edge2 = extend_rrt(nodes2, edges2, edge[1])
                if edge2 != None:
                    nodes2.append(edge2[1]) #the second node is the new node
                    edges2.append(edge2)
                    if edge2[1] == edge[1]:
                        connected = True
                        break

        else:
            edge = extend_rrt(nodes2, edges2, q_rand)
            if edge != None:
                nodes2.append(edge[1]) #the second node is the new node
                edges2.append(edge)
                tree1 = not tree1
                if edge[1] == nodes[-1]:
                    connected = True
                    break
                edge2 = extend_rrt(nodes, edges, edge[1])
                if edge2 != None:
                    nodes.append(edge2[1]) #the second node is the new node
                    edges.append(edge2)
                    if edge2[1] == edge[1]:
                        connected = True
                        break
    return (nodes, edges), (nodes2, edges2) #return Tree of nodes and edges

def extend_rrt(nodes, edges, q_rand):
    shortest_dist = 10000
    q_near = None
    for node in nodes:
        dist = edge_distance(node, q_rand)
        if dist < shortest_dist:
            q_near = node
            shortest_dist = dist

    new_edge = step_edge(q_near, q_rand)
    if valid_edge(new_edge):
        return new_edge

    return None

def step_edge(q_near, q_rand):
    if edge_distance(q_near, q_rand) <= STEP_SIZE:
        return (q_near, q_rand)
    dy = q_rand[1] - q_near[1]
    dx = q_rand[0] - q_near[0]
    theta = math.degrees(math.atan2(dy, dx))
    if theta < 0:
        theta += 360.0
    x = q_near[0] + STEP_SIZE*math.cos(math.radians(theta))
    y = q_near[1] + STEP_SIZE*math.sin(math.radians(theta))
    q_new = (x,y)
    return (q_near, q_new)

def valid_edge(edge):
    global object_list

    for obj in object_list:
        #special case when edge lies within an obstacle
        if edge[0] in obj and edge[1] in obj:
            return False

        for i in range(len(obj)):
            obj_p1 = obj[i]
            #special case when last and first vertex connect
            if i == len(obj) - 1:
                obj_p2 = obj[0]
            else:
                obj_p2 = obj[i+1]

            if intersect(edge[0], edge[1], obj_p1, obj_p2):
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
    #special cases for horizontal and vertical segments
    if (o_x1 == o_x2):
    	if intersect_vertical_obj(graph_p1, graph_p2, obj_p1, obj_p2):
    		return True
    	return False
    elif (o_y1 == o_y2):
    	if intersect_horizontal_obj(graph_p1, graph_p2, obj_p1, obj_p2):
    		return True
    	return False
    elif (g_x1 == g_x2):
    	if intersect_vertical_obj(obj_p1, obj_p2, graph_p1, graph_p2):
    		return True
    	return False
    elif (g_y1 == g_y2):
    	if intersect_horizontal_obj(obj_p1, obj_p2, graph_p1, graph_p2):
    		return True
    	return False
    #parallel lines, won't intersect
    elif (det == 0):
        return False
    #all other cases
    else:
        #intersection point
        px = abs((B2*C1 - B1*C2)/det)
        py = abs((A1*C2 - A2*C1)/det)
        #check if intersection falls within path of graph edge
        if (min(g_x1, g_x2) < px) and (max(g_x1, g_x2) > px):
            if (min(g_y1, g_y2) < py) and (max(g_y1, g_y2) > py):
                #check if intersection point falls in obstacle
                if (min(o_x1, o_x2) <= px) and (max(o_x1, o_x2) >= px):
                    if (min(o_y1, o_y2) <= py) and (max(o_y1, o_y2) >= py):
                        return True
        return False

def slope(p1, p2):
    dy = p2[1] - p1[1]
    dx = p2[0] - p1[0]

    if dx == 0:
        return None
    return float(dy/dx)

def intercept(slope, point):
    y = point[1]
    x = point[0]

    if slope == None:
        return None
    elif slope == 0.0:
        return y
    return y - (slope * x)

def intersect_horizontal_obj(segment_p1, segment_p2, obj_p1, obj_p2):
    #get y of horizontal object
    obj_y = obj_p1[1]
    #slope of edge segment
    m = slope(segment_p1, segment_p2)
    if m == None:
        #vertical line segment
        seg_x = segment_p1[0]
        if (min(obj_p1[0],obj_p2[0])<=seg_x) and (max(obj_p1[0],obj_p2[0])>=seg_x):
            if (min(segment_p1[1],segment_p2[1])<=obj_y) and (max(segment_p1[1],segment_p2[1])>=obj_y):            
                return True
        return False
    if m == 0:
        #parallel lines
        if obj_y == segment_p1[1]:
            if ((min(obj_p1[0],obj_p2[0])<=segment_p1[0]) and (max(obj_p1[0],obj_p2[0])>=segment_p1[0]) or
                (min(obj_p1[0],obj_p2[0])<=segment_p2[0]) and (max(obj_p1[0],obj_p2[0])>=segment_p2[0])):
                return True
        return False
    b = intercept(m, segment_p1)
    # calculate intersection
    x = (obj_y - b) / m
    y = obj_y

    # check if intersection falls within bounds
    if (min(obj_p1[0],obj_p2[0])<x) and (max(obj_p1[0],obj_p2[0])>x):
        if (min(segment_p1[1],segment_p2[1])<y) and (max(segment_p1[1],segment_p2[1])>y):
            return True
        elif segment_p1[1] == y or segment_p2[1] == y:
            return True
    elif obj_p1[0] == x or obj_p2[0] == x:
        if (min(segment_p1[1],segment_p2[1])<y) and (max(segment_p1[1],segment_p2[1])>y):
            return True
        elif segment_p1[1] == y or segment_p2[1] == y:
            return True
    return False

def intersect_vertical_obj(segment_p1, segment_p2, obj_p1, obj_p2):
    #get x of vertical object
    obj_x = obj_p1[0]
    #slope of edge segment
    m = slope(segment_p1, segment_p2)
    if m == None:
        #parallel lines
        if obj_x == segment_p1[0]:
            if ((min(obj_p1[1],obj_p2[1])<=segment_p1[1]) and (max(obj_p1[1],obj_p2[1])>=segment_p1[1]) or
                (min(obj_p1[1],obj_p2[1])<=segment_p2[1]) and (max(obj_p1[1],obj_p2[1])>=segment_p2[1])):
                return True
        return False
    if m == 0:
        #horizontal line segment
        seg_y = segment_p1[1]
        if (min(obj_p1[1],obj_p2[1])<=seg_y) and (max(obj_p1[1],obj_p2[1])>=seg_y):
            if (min(segment_p1[0],segment_p2[0])<=obj_x) and (max(segment_p1[0],segment_p2[0])>=obj_x):            
                return True
        return False

    b = intercept(m, segment_p1)
    # calculate intersection
    y = m * obj_x + b
    x = obj_x
    # check if intersection falls within bounds
    if (min(obj_p1[1],obj_p2[1])<y) and (max(obj_p1[1],obj_p2[1])>y):
        if (min(segment_p1[0],segment_p2[0])<x) and (max(segment_p1[0],segment_p2[0])>x):
            return True
        elif segment_p1[0] == x or segment_p2[0] == x:
            return True
    elif (obj_p1[1] == y or obj_p2[1] == y):
        if (min(segment_p1[0],segment_p2[0])<x) and (max(segment_p1[0],segment_p2[0])>x):
            return True
        elif segment_p1[0] == x or segment_p2[0] == x:
            return True
    return False

def join_trees(tree1, tree2):
    del tree2[0][-1]
    nodes = tree1[0] + tree2[0]
    edges = tree1[1] + tree2[1]
    return (nodes, edges)


def build_dict(tree):
    nodes = tree[0]
    edges = tree[1]
    nodes_dict = {}
    
    for node in nodes:
        nodes_dict[node] = []

    for edge in edges:
        nodes_dict[edge[0]].append(edge[1])
        nodes_dict[edge[1]].append(edge[0])

    return nodes_dict

def find_path(start, end, nodes, nodes_dict):
    g = dijkstra(nodes, nodes_dict, start)
    visited = g[0]
    path_dict = g[1]
    
    path_list = [end]
    path_cost = visited[end]

    node = end
    while (node != start):
        if node in path_dict:
            node = path_dict[node]
            path_list.append(node)
        else:
            print "No path exists between these two points"
            sys.exit(0)

    path_list.reverse()
    return path_list, path_cost

def dijkstra(nodes, nodes_dict, start_node):
    visited = {start_node: 0}
    path = {}

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for node in nodes_dict[min_node]:
            weight = current_weight + edge_distance(min_node, node)
            if node not in visited or weight < visited[node]:
                visited[node] = weight
                path[node] = min_node

    return visited, path

def edge_distance(p1, p2):
    y = p2[1] - p1[1]
    x = p2[0] - p1[0]
    d = math.hypot(x, y)
    return d
    
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

def draw_edges(edges):
    penup()
    for edge in edges:
        setposition(edge[0][0] * scale + offsetx, edge[0][1] * scale + offsety)
        pendown()
        setposition(edge[1][0] * scale + offsetx, edge[1][1] * scale + offsety)
        penup()

def draw_path(path_nodes):
    color('green')
    pensize(2)
    penup()

    for node in path_nodes:
        setposition(node[0] * scale + offsetx, node[1] * scale + offsety)
        pendown()

    penup()

main()