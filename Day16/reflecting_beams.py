from argparse import ArgumentParser
import numpy as np
from dataclasses import dataclass

OFFSETS = {
    'n': (-1, 0),
    's': (1, 0),
    'e': (0, 1),
    'w': (0, -1),
}

@dataclass(frozen=True)
class Beam:
    start: tuple
    dir: str

class Facility:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.height, self.width = self.grid.shape
        self.energy = np.zeros((self.height, self.width))

    def is_valid(self, loc):
        return (0 <= loc[0] < self.height) and (0 <= loc[1] < self.width)
    
    def reset_energy(self):
        self.energy = np.zeros((self.height, self.width))

    def total_energized(self):
        return np.sum(self.energy != 0)
    
    def energize(self, path):
        for loc in path:
            if self.is_valid(loc):
                self.energy[loc] += 1
    
    def find_beam_path(self, beam: Beam):
        children = []
        path = [beam.start]

        offset = OFFSETS[beam.dir]
        next_loc = (beam.start[0]+offset[0], beam.start[1]+offset[1])
        while self.is_valid(next_loc):
            if (self.grid[next_loc] in '/\\' or 
                (self.grid[next_loc] == '|' and beam.dir in 'ew') or
                (self.grid[next_loc] == '-' and beam.dir in 'ns')):
                break
            path.append(next_loc)
            next_loc = (next_loc[0]+offset[0], next_loc[1]+offset[1])

        if self.is_valid(next_loc):
            path.append(next_loc)
            if self.grid[next_loc] == '/':
                match beam.dir:
                    case 'n' | 'e':
                        next_dir = 'n' if beam.dir == 'e' else 'e'
                    case 's' | 'w':
                        next_dir = 's' if beam.dir == 'w' else 'w'
                children.append(Beam(next_loc, next_dir))
            elif self.grid[next_loc] == '\\':
                match beam.dir:
                    case 'n' | 'w':
                        next_dir = 'n' if beam.dir == 'w' else 'w'
                    case 's' | 'e':
                        next_dir = 's' if beam.dir == 'e' else 'e'
                children.append(Beam(next_loc, next_dir))
            elif self.grid[next_loc] == '|':
                children.append(Beam(next_loc, 'n'))
                children.append(Beam(next_loc, 's'))
            elif self.grid[next_loc] == '-':
                children.append(Beam(next_loc, 'e'))
                children.append(Beam(next_loc, 'w'))

        return path, children

def main(data):
    char_array = [[char for char in line] for line in data]
    facility = Facility(np.array(char_array))

    # Star 1
    beams = [Beam((0,-1), 'e')]
    seen = set()
    while beams:
        beam = beams.pop()
        path, children = facility.find_beam_path(beam)
        facility.energize(path)
        seen.add(beam)
        for child in children:
            if child not in seen:
                beams.append(child)
    print(facility.total_energized())

    # Star 2
    start_beams = []
    for row in range(facility.height):
        start_beams.append(Beam((row, -1), 'e'))
        start_beams.append(Beam((row, facility.width), 'w'))
    for col in range(facility.width):
        start_beams.append(Beam((-1, col), 's'))
        start_beams.append(Beam((facility.height, col), 'n'))

    energized = []
    for start_beam in start_beams:
        beams = [start_beam]
        seen = set()
        facility.reset_energy()
        while beams:
            beam = beams.pop()
            path, children = facility.find_beam_path(beam)
            facility.energize(path)
            seen.add(beam)
            for child in children:
                if child not in seen:
                    beams.append(child)
        energized.append(facility.total_energized())
    print(max(energized))

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
