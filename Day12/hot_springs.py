from argparse import ArgumentParser
import concurrent.futures
import re

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

def solve_extend_line(line):
    spring_row = line.split()[0]
    spring_row = '?'.join([spring_row]*5)
    sequence_lengths = all_ints(line)*5
    return count_solns(spring_row, sequence_lengths)

def main(data):
    # Star 1
    arrangements = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_line = {executor.submit(solve_line, line): (idx,line) for (idx,line) in enumerate(data)}
        for future in concurrent.futures.as_completed(future_to_line):
            idx,line = future_to_line[future]
            try:
                solns = future.result()
            except Exception as exc:
                print('%s generated an exception: %s' % (line, exc))
            else:
                #print('%s (line %d) has %d possible solns' % (line, idx, solns))
                arrangements += solns
    print(f'{arrangements} possible solutions for star 1\n')

    # Star 2
    arrangements = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_line = {executor.submit(solve_extend_line, line): (idx,line) for (idx,line) in enumerate(data)}
        for future in concurrent.futures.as_completed(future_to_line):
            idx,line = future_to_line[future]
            try:
                solns = future.result()
            except Exception as exc:
                print('%s generated an exception: %s' % (line, exc))
            else:
                print('%s (line %d) has %d possible solns' % (line, idx, solns))
                arrangements += solns
    print(f'{arrangements} possible solutions for star 2')

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
