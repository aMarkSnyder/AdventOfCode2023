from argparse import ArgumentParser
import numpy as np

class RockGrid:
    def __init__(self, data) -> None:
        self.data = data
        self.height, self.width = data.shape

    def in_bounds(self, loc):
        return (0 <= loc[0] < self.height) and (0 <= loc[1] < self.width)
    
    def final_position(self, loc):
        if self.data[loc] != 'O':
            return loc
        for row in range(loc[0]-1, -1, -1):
            if self.data[row, loc[1]] != '.':
                return (row+1, loc[1])
        return (0, loc[1])

    def roll(self, direction='n'):
        match direction:
            case 'n':
                k = 0
            case 'e':
                k = 1
            case 's':
                k = 2
            case 'w':
                k = 3
        self.data = np.rot90(self.data, k)

        for row in range(self.height):
            for col in range(self.width):
                final_pos = self.final_position((row,col))
                if final_pos != (row,col):
                    self.data[final_pos] = 'O'
                    self.data[row,col] = '.'

        if k:
            self.data = np.rot90(self.data, 4-k)

    def load(self):
        load = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.data[row,col] == 'O':
                    load += self.height - row
        return load
    
    def to_tuple(self):
        return tuple(map(tuple, self.data))

def main(data):
    char_array = [[char for char in line] for line in data]

    # Star 1
    rocks = RockGrid(np.array(char_array))
    rocks.roll()
    print(rocks.load())

    # Star 2
    rocks = RockGrid(np.array(char_array))
    spin_cycle = ('n', 'w', 's', 'e')
    observed_states = {rocks.to_tuple(): 0}
    no_cycles = 1000
    offset, repeat_len = 0, 0
    for cycle in range(1, no_cycles+1):
        for direction in spin_cycle:
            rocks.roll(direction)
        rocks_state = rocks.to_tuple()
        if rocks_state in observed_states:
            offset = observed_states[rocks_state]
            repeat_len = cycle - offset
            break
        observed_states[rocks_state] = cycle
    print(offset, repeat_len)

    total_cycles = 1000000000
    point_in_cycle = (total_cycles - offset) % repeat_len
    rocks = RockGrid(np.array(char_array))
    no_cycles = offset + point_in_cycle
    for cycle in range(1, no_cycles+1):
        for direction in spin_cycle:
            rocks.roll(direction)
    print(rocks.load())

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
