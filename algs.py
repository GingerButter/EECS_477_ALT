from preprocess import Point
from preprocess import preprocess
import heapq
import math
import copy
import random

vertices = preprocess("USA-road-d.NY")
# verticesBackup = copy.deepcopy(vertices)

def findWE(vertices):
    west = math.inf
    east = -math.inf
    w = 1
    e = 1
    for index, vertex in enumerate(vertices, start=1):
        if vertex.x < west:
            west = vertex.x
            w = index
        if vertex.x > east:
            east = vertex.x
            e = index
    return w, e

def reconstruct_path(vertices, t):
    path = []
    cur = copy.deepcopy(t)
    while cur.parent != None:
        path.append(cur.index)
        cur = vertices[cur.parent]
    path.append(cur.index)    
    path.reverse()
    return path

def coord_list(vertices, path):
    coord = []
    for i in path:
        coord.append((vertices[i].x, vertices[i].y))
    return coord

def find_landmarks(vertices, s, t, num):
    landmarks = []
    while len(landmarks) != num:
        candidate = random.randint(1, len(vertices)-1)
        if not candidate in landmarks and candidate != s:
            landmarks.append(vertices[candidate])
    return landmarks


def astar(vertices, s, t):
    openList = [] #tuple(val, point)
    openSet = set()
    vertices[s].dist = 0
    vertices[s].add_potential_astar(vertices[t])
    vertices[s].val = vertices[s].p_astar
    heapq.heappush(openList, (vertices[s].val, vertices[s]))
    openSet.add(vertices[s])
    while openList:
        _, cur = heapq.heappop(openList)
        openSet.remove(cur)
        if cur.index == t:
            return reconstruct_path(vertices, vertices[t])
        else:
            for edge in cur.next:
                ind = edge.next
                cur_dist = cur.dist + edge.dist
                if cur_dist < vertices[ind].dist:
                    vertices[ind].parent = cur.index
                    vertices[ind].dist = cur_dist
                    vertices[ind].add_potential_astar(vertices[t])
                    vertices[ind].val = vertices[ind].dist + vertices[ind].p_astar
                    if vertices[ind] not in openSet:
                        openSet.add(vertices[ind])
                        heapq.heappush(openList, (vertices[ind].val, vertices[ind]))

def alt(vertices, s, t, landmarks):
    openList = [] #tuple(val, point)
    openSet = set()
    vertices[s].dist = 0
    vertices[s].add_potential_alt(vertices[t], landmarks)
    vertices[s].val = vertices[s].p_alt
    heapq.heappush(openList, (vertices[s].val, vertices[s]))
    openSet.add(vertices[s])
    counter = 0
    while openList:
        _, cur = heapq.heappop(openList)
        openSet.remove(cur)
        counter += 1
        if cur.index == t:
            return reconstruct_path(vertices, vertices[t])
        else:
            if counter % 10000 == 0:
                print(counter)
                cur_path = reconstruct_path(vertices, cur)
                with open("cur_path_{}".format(counter), 'w') as c:
                    for i in cur_path:
                        c.write("{}\n".format(i))
            for edge in cur.next:
                ind = edge.next
                cur_dist = cur.dist + edge.dist
                if cur_dist < vertices[ind].dist:
                    vertices[ind].parent = cur.index
                    vertices[ind].dist = cur_dist
                    vertices[ind].add_potential_alt(vertices[t], landmarks)
                    vertices[ind].val = vertices[ind].dist + vertices[ind].p_alt
                    if vertices[ind] not in openSet:
                        openSet.add(vertices[ind])
                        heapq.heappush(openList, (vertices[ind].val, vertices[ind]))

# w, e = findWE(vertices)
# print(w)
# print(e)
# landmarks = find_landmarks(vertices, w, e, 10)
# print(landmarks)
# result1 = astar(vertices, 1, 4)
# result2 = alt(vertices, w, e, landmarks)

# print(result1)
# print(result1)
# with open("result2", 'w') as re:
#     for i in result2:
#         re.write("{}\n".format(i))


