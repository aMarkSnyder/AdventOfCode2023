from argparse import ArgumentParser
import networkx as nx
import matplotlib.pyplot as plt

def main(data):
    G = nx.Graph()
    for line in data:
        source, dests = line.split(': ')
        dests = dests.split()
        for dest in dests:
            G.add_edge(source, dest)

    # Finds the lowest weight (smallest, since this is unweighted) set of edges that can be
    # removed to split the graph in two. We know there will be three of them in this case.
    G.remove_edges_from(nx.minimum_edge_cut(G))
    g1, g2 = nx.connected_components(G)
    print(len(g1) * len(g2))

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
