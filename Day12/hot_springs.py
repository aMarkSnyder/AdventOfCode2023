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

def find_solns(row, sequence_lengths, solns):
    unsolved = ''.join(row).find('?')
    if unsolved == -1:
        if find_broken_sequences(row) == sequence_lengths:
            solns.append(row)
        return
    for poss_seq, true_seq in zip(find_broken_sequences(row)[:-1], sequence_lengths):
        if poss_seq != true_seq:
            return
    if row.count('?') + row.count('#') < sum(sequence_lengths):
        return
    if row.count('?') + row.count('.') < len(sequence_lengths) - 1:
        return
    fixed_path, broken_path = list(row), list(row)
    fixed_path[unsolved] = '.'
    broken_path[unsolved] = '#'
    find_solns(fixed_path, sequence_lengths, solns)
    find_solns(broken_path, sequence_lengths, solns)

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

def solve_extend_line_experiment(line):
    spring_row = line.split()[0]
    sequence_lengths = all_ints(line)
    base_solns = []
    find_solns(spring_row, sequence_lengths, base_solns)

    if len(base_solns) == 1 and base_solns[0][0] == '#' and base_solns[0][-1] == '#':
        return 1

    prepend_spring_row = '?' + spring_row
    append_spring_row = spring_row + '?'
    additional_solns = max(count_solns(prepend_spring_row,sequence_lengths), count_solns(append_spring_row, sequence_lengths))
    return len(base_solns) * additional_solns**4

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
        future_to_line = {executor.submit(solve_extend_line_experiment, line): (idx,line) for (idx,line) in enumerate(data)}
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
