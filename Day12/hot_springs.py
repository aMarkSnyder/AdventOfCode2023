from argparse import ArgumentParser
import re
import tqdm

def all_ints(s):
    return tuple(int(i) for i in re.findall(r'\b\d+\b', s))

def find_broken_sequences(row):
    sequences = []
    sequence = 0
    for char in row:
        if char == '?':
            break
        elif char == '#':
            sequence += 1
        else:
            if sequence:
                sequences.append(sequence)
                sequence = 0
    if sequence:
        sequences.append(sequence)
    return tuple(sequences)

def count_solns(row, sequence_lengths):
    unsolved = ''.join(row).find('?')
    if unsolved == -1:
        return 1 if find_broken_sequences(row) == sequence_lengths else 0
    for poss_seq, true_seq in zip(find_broken_sequences(row)[:-1], sequence_lengths):
        if poss_seq != true_seq:
            return 0
    if row.count('?') + row.count('#') < sum(sequence_lengths):
        return 0
    if row.count('?') + row.count('.') < len(sequence_lengths) - 1:
        return 0
    fixed_path, broken_path = list(row), list(row)
    fixed_path[unsolved] = '.'
    broken_path[unsolved] = '#'
    return count_solns(fixed_path, sequence_lengths) + count_solns(broken_path, sequence_lengths)

def solve_line(line):
    spring_row = line.split()[0]
    sequence_lengths = all_ints(line)
    return count_solns(spring_row, sequence_lengths)

def main(data):
    # Star 1
    arrangements = 0
    for line in data:
        spring_row = line.split()[0]
        sequence_lengths = all_ints(line)
        possible = count_solns(spring_row, sequence_lengths)
        arrangements += possible
        #print(possible)
    print(arrangements)

    arrangements = 0
    for line in tqdm.tqdm(data):
        spring_row = line.split()[0]
        spring_row = '?'.join([spring_row]*5)
        sequence_lengths = all_ints(line)*5
        possible = count_solns(spring_row, sequence_lengths)
        arrangements += possible
        #print(possible)
    print(arrangements)

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
