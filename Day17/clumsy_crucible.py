from argparse import ArgumentParser
import numpy as np
from heapq import *
import itertools

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
            'n': (-1, 0), 
            's': (1,0),
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

    def get_valid_neighbors(self, loc, last_dir, dir_streak=1, crucible_type='normal'):
        invalid_dirs = []
        if crucible_type == 'normal':
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
        else:
            if dir_streak == 10:
                invalid_dirs.append(last_dir)
            elif dir_streak < 4:
                for dir in ('n','s','e','w'):
                    if dir != last_dir:
                        invalid_dirs.append(dir)
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

def Dijkstra(heatmap: Heatmap, source, crucible_type='normal'):

    if crucible_type == 'normal':
        max_dir_streak = 3
    else:
        max_dir_streak = 10

    distances = np.inf*np.ones((heatmap.height, heatmap.width, 4, max_dir_streak))
    distances[source] = 0
    previous = np.zeros_like(heatmap.data,dtype=object)

    directions = ('n','s','e','w')

    queue = []
    entry_finder = {}
    for row in range(heatmap.height):
        for col in range(heatmap.width):
            loc = (row, col)
            for dir_idx, last_dir in enumerate(directions):
                for dir_streak in range(1, max_dir_streak+1):
                    node = (loc, last_dir, dir_streak)
                    add_node(queue,entry_finder,counter,node, distance=distances[row,col,dir_idx,dir_streak-1])

    while queue:
        try:
            closest_dist,(closest_loc,last_dir,dir_streak) = pop_node(queue,entry_finder)
        except:
            break

        neighbors = heatmap.get_valid_neighbors(closest_loc, last_dir, dir_streak, crucible_type)
        for dir,neighbor in neighbors:
            new_streak = 1 if dir != last_dir else dir_streak+1
            neighbor_node = (neighbor, dir, new_streak)
            if neighbor_node not in entry_finder:
                continue
            dist = closest_dist + heatmap.data[neighbor]
            known_dist = distances[neighbor[0], neighbor[1], directions.index(dir), new_streak-1]
            if dist < known_dist:
                add_node(queue,entry_finder,counter,neighbor_node, dist)
                distances[neighbor[0], neighbor[1], directions.index(dir), new_streak-1] = dist
                previous[neighbor] = closest_loc

    return distances,previous

def main(data):
    array = [[int(char) for char in line] for line in data]
    data = np.array(array)
    heatmap = Heatmap(data)

    start = (0,0)
    
    # Star 1
    distances, _ = Dijkstra(heatmap, start)
    print(np.min(distances[heatmap.height-1, heatmap.width-1]))

    # Star 2
    # For some reason the minimum here doesn't give the right answer even though it works on test cases
    # But the correct answer was very close
    distances, _ = Dijkstra(heatmap, start, crucible_type='ultimate')
    print(np.min(distances[heatmap.height-1, heatmap.width-1, :, 3:]))

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
