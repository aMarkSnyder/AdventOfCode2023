from argparse import ArgumentParser
import numpy as np

def weighted_manhattan(point1, point2, empty_rows, empty_cols, weight):
    row1, col1 = point1
    row2, col2 = point2

    row_range = range(row1+1, row2+1) if row2>row1 else range(row2+1, row1+1)
    col_range = range(col1+1, col2+1) if col2>col1 else range(col2+1, col1+1)

    dist = 0
    for row in row_range:
        if row in empty_rows:
            dist += weight
        else:
            dist += 1

    for col in col_range:
        if col in empty_cols:
            dist += weight
        else:
            dist += 1

    return dist

def main(data):
    char_array = [[char for char in line] for line in data]
    data = np.array(char_array)

    empty_rows = [row for row in range(data.shape[0]) if np.all(data[row,:] == '.')]
    empty_cols = [col for col in range(data.shape[1]) if np.all(data[:,col] == '.')]

    galaxies = []
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            if data[row,col] == '#':
                galaxies.append((row,col))

    for weight in (2, 10, 100, 1000000):
        total_path_length = 0
        for idx, galaxy in enumerate(galaxies):
            for second_galaxy in galaxies[idx+1:]:
                total_path_length += weighted_manhattan(galaxy, second_galaxy, empty_rows, empty_cols, weight)
        print(total_path_length)

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
