from argparse import ArgumentParser
import re
from dataclasses import dataclass
from heapq import *
import itertools
import numpy as np
from collections import defaultdict

def all_ints(s):
    return [int(i) for i in re.findall(r'\b\d+\b', s)]

REMOVED = '<removed-node>'      # placeholder for a removed node
heap_counter = itertools.count()     # unique sequence count

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

@dataclass(frozen=True)
class Block:
    idy: int
    xrange: range
    yrange: range
    zrange: range

def drop_block(grid, block):
    blocking_ids = set()
    for z in range(block.zrange.start, -1, -1):
        blocked = False
        blocking_ids = set()
        for x in block.xrange:
            for y in block.yrange:
                if grid[x,y,z] != -1:
                    blocked = True
                    blocking_ids.add(grid[x,y,z])
        if blocked:
            new_block = Block(block.idy, block.xrange, block.yrange, range(z+1, z+1+len(block.zrange)))
            supported_by = blocking_ids
            break

    for x in new_block.xrange:
        for y in new_block.yrange:
            for z in new_block.zrange:
                grid[x,y,z] = new_block.idy

    return new_block, supported_by

def main(data):
    blocks = []
    id_gen = itertools.count(1)
    entry_finder = {}
    for line in data:
        x1, y1, z1, x2, y2, z2 = all_ints(line)
        block = Block(next(id_gen), range(x1,x2+1), range(y1,y2+1), range(z1,z2+1))
        # Need a priority queue (or other iterable sorted by z) so that lower blocks fall first
        add_node(blocks, entry_finder, heap_counter, block, z1)

    # Note: input data keeps 0 <= x,y < 10, 1 <= z < 300
    grid = -1 * np.ones((10,10,300))
    grid[:,:,0] = 0
    supported_by = {}
    new_blocks = {}
    while blocks:
        _, block = pop_node(blocks, entry_finder)
        new_block, relies_on = drop_block(grid, block)
        new_blocks[new_block.idy] = new_block
        supported_by[new_block.idy] = relies_on

    supports = defaultdict(set)
    for top, bottoms in supported_by.items():
        if top not in supports:
            supports[top] = set()
        for bottom in bottoms:
            supports[bottom].add(top)

    removable = set()
    # A brick is removable if all of the blocks that it supports are also supported by other bricks
    for bottom, tops in supports.items():
        required = False
        for top in tops:
            if len(supported_by[top]) == 1:
                required = True
                break
        if not required:
            removable.add(bottom)
    print(len(removable))

    required = set(range(next(id_gen))) - removable - {0}
    total_fallen = 0
    for block_id in required:
        fallen = {block_id}
        fall_queue = list(supports[block_id])
        while fall_queue:
            poss = fall_queue.pop(0)
            no_support = True
            for supporter in supported_by[poss]:
                if supporter not in fallen:
                    no_support = False
                    break
            if no_support:
                fallen.add(poss)
                fall_queue.extend(supports[poss])
        total_fallen += len(fallen) - 1
    print(total_fallen)

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
