from argparse import ArgumentParser

def extrapolate(sequence, forward=True):
    if not any(sequence):
        return 0
    diff_seq = []
    for idx in range(1, len(sequence)):
        diff_seq.append(sequence[idx] - sequence[idx-1])
    extra_diff_val = extrapolate(diff_seq, forward)
    if forward:
        extra_val = sequence[-1] + extra_diff_val
    else:
        extra_val = sequence[0] - extra_diff_val
    return extra_val

def main(data):
    extra_vals = []
    backward_extra_vals = []
    for line in data:
        vals = [int(num) for num in line.split()]
        extra_vals.append(extrapolate(vals, forward=True))
        backward_extra_vals.append(extrapolate(vals, forward=False))
    print(sum(extra_vals))
    print(sum(backward_extra_vals))

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
