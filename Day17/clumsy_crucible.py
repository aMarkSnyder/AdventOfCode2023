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

def add_node(pq, entry_finder, counter, node, distance=0, last_dir='-', dir_streak=-1):
    'Add a new node or update an existing node'
    if node in entry_finder:
        remove_node(entry_finder,node)
    count = next(counter)
    entry = [distance, count, node, last_dir, dir_streak]
    entry_finder[node] = entry
    heappush(pq, entry)

def remove_node(entry_finder, node):
    'Mark an existing node as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(node)
    entry[-1] = REMOVED

def pop_node(pq, entry_finder):
    'Remove and return the lowest distance node. Raise KeyError if empty.'
    while pq:
        distance, count, node, last_dir, dir_streak = heappop(pq)
        if dir_streak is not REMOVED:
            del entry_finder[node]
            return distance,node,last_dir,dir_streak
    raise KeyError('pop from an empty priority queue')

def Dijkstra(heatmap: Heatmap, source):

    distances = np.inf*np.ones_like(heatmap.data)
    distances[source] = 0
    previous = np.zeros_like(heatmap.data,dtype=object)

    queue = []
    entry_finder = {}
    for row_idx,row in enumerate(distances):
        for col_idx,distance in enumerate(row):
            node = (row_idx,col_idx)
            add_node(queue,entry_finder,counter,node,distance)

    while queue:
        try:
            closest_dist,closest_node,last_dir,dir_streak = pop_node(queue,entry_finder)
        except:
            break

        dir_streak = max(0, dir_streak)
        neighbors = heatmap.get_valid_neighbors(closest_node, last_dir, dir_streak)
        for dir,neighbor in neighbors:
            if neighbor not in entry_finder:
                continue
            dist = closest_dist + heatmap.data[neighbor]
            if dist < distances[neighbor]:
                new_streak = 1 if dir != last_dir else dir_streak+1
                add_node(queue,entry_finder,counter,neighbor,dist,dir,new_streak)
                distances[neighbor] = dist
                previous[neighbor] = closest_node

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
