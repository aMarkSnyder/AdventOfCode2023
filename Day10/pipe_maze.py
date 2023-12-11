from argparse import ArgumentParser
import numpy as np
np.set_printoptions(linewidth=200)

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

def main(data):
    char_array = [[char for char in line] for line in data]
    maze = PipeMaze(np.array(char_array))

    start = np.where(maze.maze == 'S')
    start = (start[0][0], start[1][0])
    maze.maze[start] = maze.resolve_s(start)

    path = [start]
    old = start
    curr = maze.valid_neighbors(old)[0]
    while curr != start:
        path.append(curr)
        neighbors = maze.valid_neighbors(curr)
        for neighbor in neighbors:
            if neighbor != old:
                old = curr
                curr = neighbor
                break
    print(len(path)//2)

    new_maze = maze.maze
    path = set(path)
    for row in range(new_maze.shape[0]):
        for col in range(new_maze.shape[1]):
            loc = (row,col)
            if loc not in path:
                new_maze[loc] = '0'

    area = 0
    for row in range(new_maze.shape[0]):
        inside = False
        for col in range(new_maze.shape[1]):
            char = new_maze[row,col]
            # Any set of pipes that extends the loop vertically acts as an inside/outside divider.
            # The sets of pipes that do that are |, L7, and FJ.
            # Here we pick the north facing members. We could equivalently pick the south facing ones, but not both.
            if char in '|LJ':
                inside = not inside
            if char == '0' and inside:
                new_maze[row,col] = 'I'
                area += 1
    print(new_maze)
    print(area)

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
