from argparse import ArgumentParser
from collections import defaultdict

def HASH(string):
    curr = 0
    for char in string:
        curr += ord(char)
        curr *= 17
        curr %= 256
    return curr

def main(data):
    sequence = data[0].split(',')

    # Star 1
    total = 0
    for step in sequence:
        total += HASH(step)
    print(total)

    # Star 2
    boxes = defaultdict(dict)
    for step in sequence:
        instr = '-' if '-' in step else '='
        label, focal = step.split(instr)
        box_no = HASH(label)
        if instr == '-' and label in boxes[box_no]:
            del boxes[box_no][label]
        if instr == '=':
            boxes[box_no][label] = focal
    
    total_power = 0
    for box_no, box in boxes.items():
        for idx, (label, focal) in enumerate(box.items(), start=1):
            total_power += (1+box_no) * idx * int(focal)
    print(total_power)

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
