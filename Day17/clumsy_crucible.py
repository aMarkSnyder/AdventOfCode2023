from argparse import ArgumentParser
import numpy as np
from heapq import *
import itertools
import pprint

np.set_printoptions(linewidth=200)

class Heatmap:
    def __init__(self, data) -> None:
        self.data = data
        self.height, self.width = self.data.shape

    def is_valid(self, loc):
        return (0 <= loc[0] < self.height) and (0 <= loc[1] < self.width)
    
    def get_neighbors(self, loc, invalid_dirs=()):
        neighbors = set()
        moves = {
            's': (-1, 0), 
            'n': (1,0),
            'w': (0,-1),
            'e': (0,1)
        }
        for dir, offset in moves.items():
            if dir in invalid_dirs:
                continue
            candidate = (loc[0]+offset[0], loc[1]+offset[1])
            if self.is_valid(candidate):
                neighbors.add((dir, candidate))
        return neighbors

    def get_valid_neighbors(self, loc, last_dir, dir_streak=1):
        invalid_dirs = []
        if dir_streak == 3:
            invalid_dirs.append(last_dir)
        match last_dir:
            case 'n':
                invalid_dirs.append('s')
            case 's':
                invalid_dirs.append('n')
            case 'e':
                invalid_dirs.append('w')
            case 'w':
                invalid_dirs.append('e')
        return self.get_neighbors(loc, invalid_dirs)
    
REMOVED = '<removed-node>'      # placeholder for a removed node
counter = itertools.count()     # unique sequence count

def add_node(pq, entry_finder, counter, node, distance=0):
    'Add a new node or update an existing node'
    if node in entry_finder:
        remove_node(entry_finder,node)
    count = next(counter)
    entry = [distance, count, node]
    entry_finder[node] = entry
    heappush(pq, entry)

def remove_node(entry_finder, node):
    'Mark an existing node as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(node)
    entry[-1] = REMOVED

def pop_node(pq, entry_finder):
    'Remove and return the lowest distance node. Raise KeyError if empty.'
    while pq:
        distance, count, node = heappop(pq)
        if node is not REMOVED:
            del entry_finder[node]
            return distance,node
    raise KeyError('pop from an empty priority queue')

def Dijkstra(heatmap: Heatmap, source):

    distances = np.inf*np.ones_like(heatmap.data)
    distances[source] = 0
    previous = np.zeros_like(heatmap.data,dtype=object)

    queue = []
    entry_finder = {}
    for row in range(heatmap.height):
        for col in range(heatmap.width):
            loc = (row, col)
            for last_dir in ('e','n','s','w'):
                for dir_streak in (1,2,3):
                    node = (loc, last_dir, dir_streak)
                    add_node(queue,entry_finder,counter,node, distance=distances[row,col])

    while queue:
        try:
            closest_dist,(closest_loc,last_dir,dir_streak) = pop_node(queue,entry_finder)
        except:
            break

        neighbors = heatmap.get_valid_neighbors(closest_loc, last_dir, dir_streak)
        for dir,neighbor in neighbors:
            new_streak = 1 if dir != last_dir else dir_streak+1
            neighbor_node = (neighbor, dir, new_streak)
            if neighbor_node not in entry_finder:
                continue
            dist = closest_dist + heatmap.data[neighbor]
            if dist < distances[neighbor]:
                add_node(queue,entry_finder,counter,neighbor_node, dist)
                distances[neighbor] = dist
                previous[neighbor] = closest_loc

    return distances,previous

def main(data):
    array = [[int(char) for char in line] for line in data]
    data = np.array(array)
    heatmap = Heatmap(data)

    start = (0,0)
    distances, previous = Dijkstra(heatmap, start)

    pp = pprint.PrettyPrinter(width=200)
    pp.pprint(previous.tolist())

    print(distances)

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
