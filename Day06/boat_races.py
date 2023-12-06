from argparse import ArgumentParser
from math import prod
import re

def all_ints(s):
    return [int(i) for i in re.findall(r'\b\d+\b', s)]

def main(data):
    # Star 1
    times = all_ints(data[0])
    distances = all_ints(data[1])

    ways_to_win = []
    for total_time, record in zip(times,distances):
        for time in range(total_time):
            if time*(total_time-time) > record:
                ways_to_win.append(total_time - 2*time + 1)
                break
    print(prod(ways_to_win))

    # Star 2
    total_time = int(''.join(str(time) for time in times))
    record_dist = int(''.join(str(dist) for dist in distances))

    ways_to_win = 0
    for time in range(total_time):
        if time*(total_time-time) > record_dist:
            ways_to_win = total_time - 2*time + 1
            break
    print(ways_to_win)

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
