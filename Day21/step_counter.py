from argparse import ArgumentParser
import numpy as np

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
    distances = np.inf * np.ones(grid.data.shape)
    distances[start] = 0

    queue = [start]
    while queue:
        curr = queue.pop(0)
        neighbors = grid.neighbors(curr)
        for neighbor in neighbors:
            if distances[neighbor] == np.inf:
                distances[neighbor] = distances[curr] + 1
                queue.append(neighbor)
    
    return distances


def main(data):
    array = [[char for char in line] for line in data]
    data = np.array(array)

    maze = Maze(data)
    start = np.where(maze.data == 'S')
    start = (start[0][0], start[1][0])
    distances = calculate_distance(maze, start)

    exactly_64 = 0
    for row in range(maze.height):
        for col in range(maze.width):
            if distances[row,col] < 65 and not distances[row,col] % 2:
                exactly_64 += 1
    print(exactly_64)

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
