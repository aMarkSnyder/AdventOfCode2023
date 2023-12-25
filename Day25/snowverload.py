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

    #nx.draw(G, with_labels=True)
    #plt.show()

    # By inspection, the links are xxq-hqq, kgl-xzz, qfb-vkd
    G.remove_edges_from((('xxq', 'hqq'), ('kgl', 'xzz'), ('qfb', 'vkd')))
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
