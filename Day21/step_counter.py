from argparse import ArgumentParser
import numpy as np
np.set_printoptions(linewidth=300, threshold=10000)

class Maze:
    def __init__(self, data) -> None:
        self.data = data
        self.height, self.width = self.data.shape

    def is_valid(self, loc):
        return (0 <= loc[0] < self.height) and (0 <= loc[1] < self.width)
    
    def neighbors(self, loc):
        neighbors = []
        for offset in [(0,1), (0,-1), (-1,0), (1,0)]:
            neighbor = (loc[0]+offset[0], loc[1]+offset[1])
            if self.is_valid(neighbor) and self.data[neighbor] != '#':
                neighbors.append(neighbor)
        return neighbors

def calculate_distance(grid: Maze, start, steps=64):
    distances = -1 * np.ones(grid.data.shape, dtype=int)
    distances[start] = 0

    queue = [start]
    while queue:
        curr = queue.pop(0)
        neighbors = grid.neighbors(curr)
        for neighbor in neighbors:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[curr] + 1
                queue.append(neighbor)
    
    return distances

def grid_index(grid, loc, base_size):
        return grid[base_size*loc[0]:base_size*(loc[0]+1), base_size*loc[1]:base_size*(loc[1]+1)]
    
def count_reachable(distances, step_goal):
    if step_goal % 2:
        return np.sum((distances!=-1).astype(int) * distances%2 * (distances<=step_goal).astype(int))
    else:
        return np.sum((distances!=-1).astype(int) * (1-distances%2) * (distances<=step_goal).astype(int))
    
def count_parity(distances):
    even, odd = np.sum((distances!=-1).astype(int) * (1-distances%2)), np.sum((distances!=-1).astype(int) * distances%2)
    return even, odd

def count_axis(axis_grid, step_goal, parity_counts, diagonal_check=False):
    # Returns the number of valid tiles at the edge n/e/s/w and total extent in that direction
    size = axis_grid.shape[0]
    parity = step_goal % 2

    # We need to add enough grids to make it so the step goal is in the outside grid
    added_grids = (step_goal - np.min(axis_grid[axis_grid>=0])) // size
    if added_grids < 0:
        return 0, 1
    offset = added_grids * size
    edge_grid = axis_grid + offset*np.ones_like(axis_grid)*(axis_grid>=0).astype(int)
    count = count_reachable(edge_grid, step_goal)

    if diagonal_check:
        partially_full = axis_grid + (offset-size)*np.ones_like(axis_grid)*(axis_grid>=0).astype(int)
        diagonal_count = count_reachable(partially_full, step_goal)
        if diagonal_count not in parity_counts.values():
            return diagonal_count, added_grids
        else:
            return 0, added_grids

    # if added_grids % 2:
    #     count += added_grids//2 * parity_counts[parity]
    #     count += (added_grids//2 + 1) * parity_counts[1-parity]
    # else:
    #     count += added_grids * (parity_counts[0] + parity_counts[1]) // 2
    return count, added_grids+1

def main(data):
    array = [[char for char in line] for line in data]
    data = np.array(array)

    start = np.where(data == 'S')
    start = (start[0][0], start[1][0])
    data[start] = '.'

    # Star 1
    maze = Maze(data)
    distances = calculate_distance(maze, start)

    exactly_64 = 0
    for row in range(maze.height):
        for col in range(maze.width):
            if distances[row,col] < 65 and not distances[row,col] % 2:
                exactly_64 += 1
    print(exactly_64)

    # Star 2
    step_goal = 500
    size = maze.height
    buffered_data = np.tile(data, (3,3))
    buffered_start = (start[0]+size, start[1]+size)
    buffered_distances = calculate_distance(Maze(buffered_data), buffered_start)
    # for row in range(0, buffered_distances.shape[0], size):
    #     for col in range(0, buffered_distances.shape[1], size):
    #         buffered_distances[row,col] += 100
    # print(buffered_distances)

    # In the infinite grid, it takes a constant number of steps (the grid size) to move from one block to the same
    # position in the next block in any direction within a quadrant. It only gets messy when you cross an axis going
    # through the starting position. This means that for each quadrant, the outermost blocks are identical.
    # If the grid size is odd (it is), the tiles that are reachable for filled grids will flip each grid.

    # Also, looking at my own input, the row and column of the start, as well as all along the edge, are completely empty 
    # of obstacles. So maybe I actually don't need special treatment of the start block for my own input?
    dist_grids = {}
    for row in range(3):
        for col in range(3):
            dist_grids[(row-1,col-1)] = grid_index(buffered_distances, (row,col), size)

    start_even, start_odd = count_parity(dist_grids[(0,0)])
    parity = step_goal % 2
    parity_counts = {0: start_even, 1: start_odd}
    print(parity_counts)

    total_valid = 0
    dir_lens = {}
    for offset in [(-1,0),(1,0),(0,1),(0,-1)]:
        valid, dir_len = count_axis(dist_grids[offset], step_goal, parity_counts)
        print(f'adding {valid} for the edge {dir_len} away in direction {offset}')
        total_valid += valid
        dir_lens[offset] = dir_len
    print(total_valid)

    for offset in [(-1,-1),(1,-1),(-1,1),(1,1)]:
        dist_grid = dist_grids[offset]
        outer_edge_count, corner_extent = count_axis(dist_grid, step_goal, parity_counts)
        inner_edge_count, inner_extent = count_axis(dist_grid, step_goal, parity_counts, diagonal_check=True)
        print(f'found that each outer quadrant edge grid {corner_extent} away in quadrant {offset} contributes {outer_edge_count}')
        print(f'adding {corner_extent} of those')
        print(f'found that each inner quadrant edge grid {inner_extent} away in quadrant {offset} contributes {inner_edge_count}')
        print(f'adding {inner_extent} of those')
        total_valid += (corner_extent) * outer_edge_count
        total_valid += (inner_extent) * inner_edge_count
    print(total_valid)

    filled_in = (corner_extent+1)**2
    if filled_in % 2:
        total_valid += parity_counts[parity] * (filled_in//2 + 1)
        total_valid += parity_counts[1-parity] * filled_in//2
    else:
        total_valid += parity_counts[parity] * filled_in//2
        total_valid += parity_counts[1-parity] * filled_in//2
    print(total_valid)


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
