import math

class Node:
    def __init__(self, coords, parent=None, g=0, h=0):
        self.coords = coords
        self.parent = parent
        self.g = g
        self.h = h
        self.f_cost = g + h

def IDA_Star(root, goal, graph):
    root_node = Node(root, None, 0, heuristic(root, goal))
    f_limit = root_node.f_cost #changed this to the f_cost or else im gonna forget about it later lol

    while True:
        solution, new_limit = DFS_Contour(root_node, goal, graph, f_limit)
        if solution:
            return rev_path(solution)
        if new_limit == math.inf:
            return None
        f_limit = new_limit

def DFS_Contour(node, goal, graph, f_limit):
    if node.f_cost > f_limit:
        return None, node.f_cost
    if goal_test(node.coords, goal):
        return node, f_limit

    next_f = math.inf
    for succ in get_successors(node, goal, graph):
        solution, new_f = DFS_Contour(succ, goal, graph, f_limit)
        if solution:
            return solution, f_limit
        next_f = min(next_f, new_f)
    return None, next_f

def goal_test(node, goal):
    if hasattr(goal, "loc"):
        gx, gy = goal.loc
    else:
        gx, gy = goal
    return node == (gx, gy)

def get_successors(node, goal, graph):
    successors = []
    movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    max_y = len(graph)
    max_x = len(graph[0])
    for dx, dy in movements:
        nx = node.coords[0] + dx
        ny = node.coords[1] + dy
        if graph[ny][nx] != 1:
            g = node.g + 1
            h = heuristic((nx, ny), goal)
            successors.append(Node((nx, ny), node, g, h))
    return successors

def heuristic(node, goal):
    # manhattan distance heuristic
    if hasattr(goal, "loc"):
        gx, gy = goal.loc
    else:
        gx, gy = goal
    return abs(node[0] - gx) + abs(node[1] - gy)

def rev_path(node):
    path = []
    while node:
        path.append(node.coords)
        node = node.parent
    return list(reversed(path))

#def main():
#   root = (1, 1)
#    goal = (3, 3)
#    graph = [
#        [1,1,1,1,1],
 #       [1,0,1,0,1],
#        [1,0,0,0,1],
 #       [1,0,1,0,1],
 #       [1,1,1,1,1]
 #   ]

 #   path = IDA_Star(root, goal, graph)
 #   if path:
 #       print("path found:", path)
 #   else:
 #       print("no path found")

#main()
