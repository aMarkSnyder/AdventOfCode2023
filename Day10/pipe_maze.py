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

    inside = 0
    for row in range(new_maze.shape[0]):
        bottoms = 0
        tops = 0
        for col in range(new_maze.shape[1]):
            char = new_maze[row,col]
            # A bottom leading to another bottom can't enclose because it's a solid bottom side of the loop
            if char in '|LJ':
                bottoms += 1
            # A top leading to another top also can't enclose
            if char in '|F7':
                tops += 1
            if char == '0':
                # But a paired bottom and top CAN enclose, because they extend the loop further vertically
                # Obviously a wall also does that which is why it affects both counters, just like a paired bottom/top
                if (bottoms % 2) and (tops % 2):
                    new_maze[row,col] = 'I'
                    inside += 1
    print(new_maze)
    print(inside)

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
