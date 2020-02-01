import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
    G = nx.Graph()
    G.add_node(1)
    G.add_nodes_from([2, 3])
    G.add_edge(1, 2)
    e = (2, 3)
    G.add_edge(*e)
    G.add_edges_from([(1, 2), (1, 3)])
    G.clear()

    G.add_edges_from([(1, 2), (1, 3)])
    G.add_node(1)
    G.add_edge(1, 2)
    G.add_node("spam")  # adds node "spam"
    G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
    G.add_edge(3, 'm')
    print( list(G.nodes))

    FG = nx.Graph()
    FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])

    MG = nx.MultiGraph()