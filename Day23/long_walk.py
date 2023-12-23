from argparse import ArgumentParser
import numpy as np
import networkx as nx

class Maze:
    def __init__(self, data) -> None:
        self.data = data
        self.height, self.width = self.data.shape

    def is_valid(self, loc):
        return (
            (0 <= loc[0] < self.height) and 
            (0 <= loc[1] < self.width) and
            self.data[loc] != '#'
        )
    
    def neighbors(self, loc, seen):
        neighbors = []
        match self.data[loc]:
            case '.':
                offsets = [(0,1), (0,-1), (-1,0), (1,0)]
            case '<':
                offsets = [(0,-1)]
            case '>':
                offsets = [(0,1)]
            case '^':
                offsets = [(-1,0)]
            case 'v':
                offsets = [(1,0)]
            case _:
                offsets = []
        for offset in offsets:
            neighbor = (loc[0]+offset[0], loc[1]+offset[1])
            if self.is_valid(neighbor) and neighbor not in seen:
                neighbors.append(neighbor)
        return neighbors
    
def build_graph(maze, start, goal, part1=True):
    if part1:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    for node in (start, goal):
        G.add_node(node)
    for row in range(maze.height):
        for col in range(maze.width):
            if len(maze.neighbors((row,col), set())) in (3,4):
                G.add_node((row,col))

    for node in G.nodes:
        queue = []
        neighbors = maze.neighbors(node, set())
        for neighbor in neighbors:
            queue.append((neighbor, 1, {node}))
        while queue:
            curr_loc, curr_dist, curr_seen = queue.pop(0)
            neighbors = maze.neighbors(curr_loc, curr_seen)
            for neighbor in neighbors:
                if neighbor in G.nodes:
                    G.add_edge(node, neighbor, weight=curr_dist+1)
                else:
                    next_seen = set(curr_seen)
                    next_seen.add(curr_loc)
                    queue.append((neighbor, curr_dist+1, next_seen))

    return G

def main(data):
    array = [[char for char in line] for line in data]
    data = np.array(array)

    maze = Maze(data)
    start = (0, 1)
    goal = (maze.height-1, maze.width-2)

    G = build_graph(maze, start, goal)
    print(max((nx.path_weight(G, path, 'weight') for path in nx.all_simple_paths(G, start, goal))))

    maze.data[maze.data != '#'] = '.'
    G = build_graph(maze, start, goal, part1=False)
    print(max((nx.path_weight(G, path, 'weight') for path in nx.all_simple_paths(G, start, goal))))

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
