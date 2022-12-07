import math
import heapq

class Edge:
    def __init__(self, next, dist):
        self.next = next
        self.dist = dist
    
    def __str__(self) -> str:
        return "next: {}, dist: {}".format(self.next, self.dist)


class Point:
    def __init__(self):
        self.index = -1
        self.x = math.inf
        self.y = math.inf
        self.dist = math.inf
        self.p_astar = math.inf
        self.p_alt = math.inf
        self.val = math.inf #dist + potential
        self.open = True
        self.parent = None
        self.next = list()
    
    def __str__(self) -> str:
        return "index: {}, x: {}, y: {}\nnext: {}".format(self.index, self.x, self.y, self.next)

    def add_edge(self, next, dist):
        self.next.append(Edge(next, dist))

    def add_potential_astar(self, other):
        self.p_astar = math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    def add_potential_alt(self, other, landmarks):
        min_p = math.inf
        for i in landmarks:
            cur_p = self.euclidean_dist(other) + other.euclidean_dist(i)
            min_p = min(cur_p, min_p)
        self.p_alt = min_p

    def euclidean_dist(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

def preprocess(dataName):
    vertices = list()
    vertices.append(Point()) #dummy
    with open("{}.co".format(dataName), 'r') as co:
        while True:
            line = co.readline()
            if not line: break
            tokens = line.strip().split(' ')
            if tokens[0] == 'v':
                vertices.append(Point())
                vertices[-1].index = int(tokens[1])
                vertices[-1].x = float(tokens[2])
                vertices[-1].y = float(tokens[3])
    with open("{}.gr".format(dataName), 'r') as gr:
        while True:
            line = gr.readline()
            if not line: break
            tokens = line.strip().split(' ')
            if tokens[0] == 'a':
                fr = int(tokens[1])
                to = int(tokens[2])
                vertices[fr].add_edge(to, float(tokens[3]))
    return vertices

