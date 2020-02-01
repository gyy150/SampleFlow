import networkx as nx
import matplotlib.pyplot as plt
import Process_CSV


if __name__ == "__main__":
    #  edge directed graph
    G = nx.DiGraph()
    Adjancency_Matrix = Process_CSV.calculate_adjacency_matrix()

    with open('MachineID_MachineName.txt', mode='r') as Machine_file:
        machine_id_list = []
        machine_id_list.append(0)
        machine_name_list = []
        machine_name_list.append('start')
        for line in Machine_file:
            s_line = line.split('        ')
            if len(s_line) > 1:
                machine_id = s_line[0]
                machine_id_list.append(machine_id)
                machine_name = s_line[1].strip()
                machine_name_list.append(machine_name)



    for i in range(len(machine_name_list)):
        G.add_node(i,name = machine_name_list[i])


    for i in range(len(Adjancency_Matrix)):
        for j in range(len(Adjancency_Matrix)):
            if Adjancency_Matrix[i][j] > 5:
                G.add_edge(i, j, sample_count= Adjancency_Matrix[i][j])



    print(G.nodes.data())
    isolated_nodes = list(nx.isolates(G))
    nonisolated_nodes = [ ]
    for node in G.nodes:
        if node not in isolated_nodes:
            nonisolated_nodes.append(node)
    isolated_machines = [G.nodes[x]['name'] for x in isolated_nodes]
    print(isolated_machines)

    end_nodes = []
    for node in nonisolated_nodes:
        print(G.nodes[node]['name'])
        neighbors = list(G.neighbors(node))
        print(neighbors)
        predecessors = list(G.predecessors(node))
        print(predecessors)
        print(list(G.out_edges(node)))
        print(list(G.in_edges(node)))
        if len(neighbors) == 1 and len(predecessors) == 1 and neighbors[0] == predecessors[0]:
            end_nodes.append(node)
    print( [G.nodes[x]['name'] for x in end_nodes])




    edges = G.edges()
    weights = [G[u][v]['sample_count'] for u, v in edges]
    weights = [weight / max(weights) * 5 for weight in weights]
    nx.draw(G,
            pos=nx.spring_layout(G),
            labels=nx.get_node_attributes(G, 'name'),
            nodelist=nonisolated_nodes,
            font_size=8,
            node_size=75,
            width=weights,
            edge_color='r'
            )
    plt.show()