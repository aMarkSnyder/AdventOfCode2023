import numpy as np
from math import prod
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class EnginePart():
    value: int
    row: int
    left: int
    right: int

    def get_neighbors(self, schematic: np.array):
        neighbors = set()
        for col in range(self.left-1, self.right+2):
            if is_valid_idx(schematic, (self.row-1, col)):
                neighbors.add((self.row-1, col))
            if is_valid_idx(schematic, (self.row+1, col)):
                neighbors.add((self.row+1, col))
        if is_valid_idx(schematic, (self.row, self.left-1)):
            neighbors.add((self.row, self.left-1))
        if is_valid_idx(schematic, (self.row, self.right+1)):
            neighbors.add((self.row, self.right+1))

        return neighbors

    def contains(self, idx):
        row, col = idx
        return (row == self.row) and (self.left <= col <= self.right)
    
    def get_potential_gears(self, schematic: np.array):
        neighbors = self.get_neighbors(schematic)
        gears = set()
        for neighbor in neighbors:
            if schematic[neighbor] == '*':
                gears.add(neighbor)
        return gears

def is_valid_idx(schematic: np.array, idx: tuple):
    height, width = schematic.shape
    if not 0 <= idx[0] < height:
        return False
    if not 0 <= idx[1] < width:
        return False
    return True

def get_part(schematic: np.array, idx: tuple):
    if not schematic[idx].isdigit():
        return None
    
    row, col = idx
    
    left = col
    while is_valid_idx(schematic, (idx[0], left-1)) and schematic[(idx[0], left-1)].isdigit():
        left -= 1

    right = col
    while is_valid_idx(schematic, (idx[0], right+1)) and schematic[(idx[0], right+1)].isdigit():
        right += 1

    value = int(''.join(schematic[row, left:right+1]))
    part = EnginePart(value, row, left, right)
    for neighbor in part.get_neighbors(schematic):
        if not schematic[neighbor].isdigit() and not schematic[neighbor] == '.':
            return part
    return None

def main():
    schematic = []
    with open('input.txt','r') as input:
        for line in input:
            schematic.append([char for char in line.strip()])
    schematic = np.array(schematic)

    # Star 1
    parts = []
    last_part = EnginePart(-1,-1,-1,-1)
    for row in range(schematic.shape[0]):
        for col in range(schematic.shape[1]):
            if not last_part.contains((row,col)):
                part = get_part(schematic, (row, col))
                if part is not None:
                    parts.append(part)
                    last_part = part

    print(sum(part.value for part in parts))

    # Star 2
    potential_gears = defaultdict(list)
    for part in parts:
        for gear in part.get_potential_gears(schematic):
            potential_gears[gear].append(part.value)

    total_gear_ratio = 0
    for gear, values in potential_gears.items():
        if len(values) == 2:
            total_gear_ratio += prod(values)
    
    print(total_gear_ratio)

if __name__ == '__main__':
    main()