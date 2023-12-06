from argparse import ArgumentParser
from math import prod

def main(data):
    # Star 1
    times = [int(time) for time in data[0].split(':')[1].split()]
    distances = [int(dist) for dist in data[1].split(':')[1].split()]

    ways_to_win = []
    for total_time, record in zip(times,distances):
        for time in range(total_time):
            if time*(total_time-time) > record:
                ways_to_win.append(total_time - 2*time + 1)
                break
    print(prod(ways_to_win))

    # Star 2
    total_time = int(data[0].split(':')[1].replace(' ', ''))
    record_dist = int(data[1].split(':')[1].replace(' ', ''))

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
