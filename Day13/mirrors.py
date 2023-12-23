from argparse import ArgumentParser
import numpy as np

def find_reflections(line):
    reflections = []
    for idx in range(1, len(line)):
        behind = line[:idx][::-1]
        ahead = line[idx:]
        valid = True
        for b,a in zip(behind,ahead):
            if b != a:
                valid = False
                break
        if valid:
            reflections.append(idx)
    return reflections

def main(data):
    patterns = []
    pattern = []
    for line in data:
        if line == '':
            patterns.append(np.array(pattern))
            pattern = []
        else:
            pattern.append([char for char in line])
    patterns.append(np.array(pattern))
    
    # Star 1
    horis = []
    verts = []
    for pattern in patterns:
        hori_refs = np.zeros(pattern.shape)
        vert_refs = np.zeros(pattern.shape)
        for idx, row in enumerate(pattern):
            reflections = find_reflections(row)
            hori_refs[idx, reflections] = 1
        for idx, col in enumerate(pattern.T):
            reflections = find_reflections(col)
            vert_refs[reflections, idx] = 1
        for idx, col in enumerate(hori_refs.T):
            if np.all(col):
                verts.append(idx)
        for idx, row in enumerate(vert_refs):
            if np.all(row):
                horis.append(idx)
    
    summary = 0
    for loc in horis:
        summary += 100*loc
    for loc in verts:
        summary += loc
    print(summary)

    # Star 2
    horis = []
    verts = []
    for pattern in patterns:
        hori_refs = np.zeros(pattern.shape)
        vert_refs = np.zeros(pattern.shape)
        for idx, row in enumerate(pattern):
            reflections = find_reflections(row)
            hori_refs[idx, reflections] = 1
        for idx, col in enumerate(pattern.T):
            reflections = find_reflections(col)
            vert_refs[reflections, idx] = 1
        for idx, col in enumerate(hori_refs.T):
            if np.sum(col) == len(col)-1:
                verts.append(idx)
        for idx, row in enumerate(vert_refs):
            if np.sum(row) == len(row)-1:
                horis.append(idx)
    
    summary = 0
    for loc in horis:
        summary += 100*loc
    for loc in verts:
        summary += loc
    print(summary)


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
