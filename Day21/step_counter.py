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
    buffered_data = np.tile(data, (3,3))
    buffered_start = (start[0]+2*maze.height, start[1]+2*maze.width)
    buffered_distances = calculate_distance(Maze(buffered_data), buffered_start)
    # for coord in [(0,0),(11,0),(22,0),(0,11),(11,11),(22,11),(0,22),(11,22),(22,22)]:
    #     buffered_distances[coord] += 100
    # print(buffered_distances)

    # In the infinite grid, it takes a constant number of steps (the grid size) to move from one block to the same
    # position in the next block in any direction within a quadrant. It only gets messy when you cross an axis going
    # through the starting position. This means that for each quadrant, the outermost blocks are identical.
    # If the grid size is odd (it is), the tiles that are reachable for filled grids will flip each grid.
    


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
