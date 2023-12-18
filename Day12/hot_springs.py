from argparse import ArgumentParser
from functools import cache

@cache
def count_solns(row, sequence_lengths, curr_streak=0):
    if not sequence_lengths and not row:
        return 1
    if not sequence_lengths:
        if row.count('#') == 0:
            return 1
        return 0
    if not row:
        if len(sequence_lengths) == 1 and curr_streak == sequence_lengths[0]:
            return 1
        return 0
    if curr_streak > sequence_lengths[0]:
        return 0
    match row[0]:
        case '.':
            if curr_streak:
                return 0 if curr_streak != sequence_lengths[0] else count_solns(row[1:], sequence_lengths[1:], 0)
            else:
                return count_solns(row[1:], sequence_lengths, 0)
        case '#':
            return count_solns(row[1:], sequence_lengths, curr_streak+1)
        case '?':
            return (count_solns('.' + row[1:], sequence_lengths, curr_streak) 
                    + count_solns('#' + row[1:], sequence_lengths, curr_streak))

def main(data):
    arrangements = 0
    arrangements2 = 0
    for line in data:
        row, sequence_lengths = line.split()
        sequence_lengths = tuple(int(length) for length in sequence_lengths.split(','))
        arrangements += count_solns(row, sequence_lengths)
        arrangements2 += count_solns('?'.join([row]*5), sequence_lengths*5)
    print(arrangements)
    print(arrangements2)

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
