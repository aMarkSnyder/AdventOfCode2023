from argparse import ArgumentParser
from itertools import cycle
from math import lcm

def main(data):
    nodes = {}
    for line in data[2:]:
        nodes[line[0:3]] = (line[7:10], line[12:15])
    
    # Star 1
    turns = cycle(data[0])
    curr = 'AAA'
    for step, turn in enumerate(turns, start=1):
        curr = nodes[curr][0] if turn == 'L' else nodes[curr][1]
        if curr == 'ZZZ':
            print(step)
            break

    # Star 2
    starts = [node for node in nodes if node.endswith('A')]
    lengths = []
    for start in starts:
        turns = cycle(data[0])
        curr = start
        for step, turn in enumerate(turns, start=1):
            curr = nodes[curr][0] if turn == 'L' else nodes[curr][1]
            if curr.endswith('Z'):
                lengths.append(step)
                break
    print(lcm(*lengths))

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
