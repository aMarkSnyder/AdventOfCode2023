from argparse import ArgumentParser
from dataclasses import dataclass
import numpy as np

OFFSETS = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}

class PipeMaze():
    def __init__(self, maze) -> None:
        self.maze = maze

    def resolve_s(self, loc):
        if self.maze[loc] != 'S':
            return self.maze[loc]
        neighbors = self.neighbors(loc)
        valid = []
        for dir, neighbor in neighbors.items():
            if dir == 'n' and self.maze[neighbor] in ('|', '7', 'F'):
                valid.append(dir)
            elif dir == 'e' and self.maze[neighbor] in ('-', 'J', '7'):
                valid.append(dir)
            elif dir == 's' and self.maze[neighbor] in ('|', 'L', 'J'):
                valid.append(dir)
            elif dir == 'w' and self.maze[neighbor] in ('-', 'L', 'F'):
                valid.append(dir)
        valid = tuple(valid)
        match valid:
            case ('n', 's'):
                return '|'
            case ('e', 'w'):
                return '-'
            case ('n', 'e'):
                return 'L'
            case ('n', 'w'):
                return 'J'
            case ('s', 'w'):
                return '7'
            case ('e', 's'):
                return 'F'
            case _:
                return '.'

    def neighbors(self, loc):
        neighbors = {}
        if loc[0]-1 >= 0:
            neighbors['n'] = ((loc[0]-1, loc[1]))
        if loc[1]+1 < self.maze.shape[1]:
            neighbors['e'] = ((loc[0], loc[1]+1))
        if loc[0]+1 < self.maze.shape[0]:
            neighbors['s'] = ((loc[0]+1, loc[1]))
        if loc[1]-1 >= 0:
            neighbors['w'] = ((loc[0], loc[1]-1))
        return neighbors

    def valid_neighbors(self, loc):
        char = self.resolve_s(loc)
        neighbors = self.neighbors(loc)
        match char:
            case '|':
                valid = ('n', 's')
            case '-':
                valid = ('e', 'w')
            case 'L':
                valid = ('n', 'e')
            case 'J':
                valid = ('n', 'w')
            case '7':
                valid = ('s', 'w')
            case 'F':
                valid = ('e', 's')
            case _:
                valid = ()
        return tuple(neighbors[valid_dir] for valid_dir in valid)

def get_pipe_shape(last_dir, curr_dir):
    if last_dir == curr_dir and curr_dir in 'UD':
        return '|'
    elif last_dir == curr_dir and curr_dir in 'LR':
        return '-'
    elif last_dir == 'U' and curr_dir == 'L':
        return '7'
    elif last_dir == 'U' and curr_dir == 'R':
        return 'F'
    elif last_dir == 'D' and curr_dir == 'L':
        return 'J'
    elif last_dir == 'D' and curr_dir == 'R':
        return 'L'
    elif last_dir == 'L' and curr_dir == 'U':
        return 'L'
    elif last_dir == 'L' and curr_dir == 'D':
        return 'F'
    elif last_dir == 'R' and curr_dir == 'U':
        return 'J'
    elif last_dir == 'R' and curr_dir == 'D':
        return '7'
    return 'S'

@dataclass
class Instruction:
    direction: str
    length: int
    color: str

def main(data):
    instructions = []
    for line in data:
        split = line.split()
        instructions.append(Instruction(split[0], int(split[1]), split[2][2:8]))

    arena = np.zeros((2000,2000), dtype='<U1')
    for row in range(arena.shape[0]):
        for col in range(arena.shape[1]):
            arena[row,col] = '0'
    start = (1000,1000)

    # Star 1 - using pipe maze code from day 10
    curr_pos = start
    curr_dir = 'B'
    path = {start}
    for instruction in instructions:
        last_dir = curr_dir
        curr_dir = instruction.direction
        arena[curr_pos] = get_pipe_shape(last_dir, curr_dir)
        offset = OFFSETS[curr_dir]
        for _ in range(instruction.length):
            curr_pos = (curr_pos[0] + offset[0], curr_pos[1] + offset[1])
            path.add(curr_pos)
            arena[curr_pos] = get_pipe_shape(curr_dir, curr_dir)
    arena[start] = 'S'
    arena[start] = PipeMaze(arena).resolve_s(start)

    for row in range(arena.shape[0]):
        inside = False
        for col in range(arena.shape[1]):
            char = arena[row,col]
            if char in '|LJ':
                inside = not inside
            if char == '0' and inside:
                arena[row,col] = 'I'
    
    print(np.sum(arena != '0'))

    # Star 2
    new_instructions = []
    for instruction in instructions:
        color = instruction.color
        length = int(color[:-1], 16)
        direction = list(OFFSETS.keys())[int(color[-1], 16)]
        new_instructions.append(Instruction(direction, length, color))
    instructions = new_instructions

    path_length = 0
    curr_pos = (0,0)
    vertices = [curr_pos]
    for instruction in instructions:
        path_length += instruction.length
        offset = OFFSETS[instruction.direction]
        total_offset = (instruction.length*offset[0],  instruction.length*offset[1])
        curr_pos = (curr_pos[0]+total_offset[0], curr_pos[1]+total_offset[1])
        vertices.append(curr_pos)

    # Shoelace formula to find area of interior, but why is this just interior and not total?
    # I think it's because only half the vertices are actually on the outside of the filled area
    area = 0
    for idx, vertex in enumerate(vertices[:-1]):
        area += (vertex[1] + vertices[idx+1][1]) * (vertex[0] - vertices[idx+1][0])
    area /= 2

    # Pick's theorem, but why does it turn out to be +1 here and not -1 like it should be?
    print(abs(area) + path_length/2 + 1)

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
