from argparse import ArgumentParser
import numpy as np
from collections import defaultdict
from copy import copy
import itertools
from heapq import *

heap_counter = itertools.count()     # unique sequence count

def add_node(pq, node, distance=0):
    'Add a new node'
    count = next(heap_counter)
    entry = [distance, count, node]
    heappush(pq, entry)

def pop_node(pq):
    'Remove and return the lowest distance node. Raise KeyError if empty.'
    while pq:
        distance, _, node = heappop(pq)
        return distance,node
    raise KeyError('pop from an empty priority queue')

class Maze:
    def __init__(self, data) -> None:
        self.data = data
        self.height, self.width = self.data.shape

    def is_valid(self, loc):
        return (
            (0 <= loc[0] < self.height) and 
            (0 <= loc[1] < self.width) and
            self.data[loc] != '#'
        )
    
    def neighbors(self, loc, seen):
        neighbors = []
        match self.data[loc]:
            case '.':
                offsets = [(0,1), (0,-1), (-1,0), (1,0)]
            case '<':
                offsets = [(0,-1)]
            case '>':
                offsets = [(0,1)]
            case '^':
                offsets = [(-1,0)]
            case 'v':
                offsets = [(1,0)]
            case _:
                offsets = []
        for offset in offsets:
            neighbor = (loc[0]+offset[0], loc[1]+offset[1])
            if self.is_valid(neighbor) and neighbor not in seen:
                neighbors.append(neighbor)
        return neighbors

def main(data):
    array = [[char for char in line] for line in data]
    data = np.array(array)

    maze = Maze(data)
    start = (0, 1)
    goal = (maze.height-1, maze.width-2)
    seen = set()
    
    curr_max = 0
    queue = [(start, 0, seen)]
    while queue:
        curr_loc, curr_dist, curr_seen = queue.pop(0)
        neighbors = maze.neighbors(curr_loc, curr_seen)
        for neighbor in neighbors:
            if neighbor == goal:
                if curr_dist+1 > curr_max:
                    curr_max = curr_dist+1
            else:
                next_seen = set(curr_seen)
                next_seen.add(curr_loc)
                queue.append((neighbor, curr_dist+1, next_seen))
    print(curr_max)

    data[data != '#'] = '.'
    nodes = set([start, goal])
    for row in range(maze.height):
        for col in range(maze.width):
            if len(maze.neighbors((row,col), set())) in (3,4):
                nodes.add((row,col))

    edges = defaultdict(dict)
    for node in nodes:
        queue = []
        neighbors = maze.neighbors(node, set())
        for neighbor in neighbors:
            queue.append((neighbor, 1, {node}))
        while queue:
            curr_loc, curr_dist, curr_seen = queue.pop(0)
            neighbors = maze.neighbors(curr_loc, curr_seen)
            for neighbor in neighbors:
                if neighbor in nodes:
                    edges[node][neighbor] = curr_dist + 1
                else:
                    next_seen = set(curr_seen)
                    next_seen.add(curr_loc)
                    queue.append((neighbor, curr_dist+1, next_seen))

    curr_max = 0
    queue = []
    nodes.discard(start)
    for node, dist in edges[start].items():
        new_nodes = copy(nodes)
        add_node(queue, (node, dist, new_nodes), -dist)
    while queue:
        _, (curr_loc, curr_dist, curr_nodes) = pop_node(queue)
        # We can never return to the node we're using
        curr_nodes.discard(curr_loc)
        neighbors = edges[curr_loc]
        if goal in neighbors:
            if curr_dist + neighbors[goal] > curr_max:
                print(f'found new max distance {curr_dist + neighbors[goal]}')
                curr_max = curr_dist + neighbors[goal]
        else:
            for neighbor,dist in neighbors.items():
                if neighbor in curr_nodes:
                    new_nodes = copy(curr_nodes)
                    add_node(queue, (neighbor, curr_dist+dist, new_nodes), -(curr_dist+dist))
    print(curr_max)

def read_input(input_file):
    data = []
    with open(input_file, 'r') as input:
        for line in input:
            data.append(line.strip())
    return data

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input_file', nargs='?', default='input.txt')
    args = parser.parse_args()
    data = read_input(args.input_file)
    main(data)
