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
    print(G.out_edges([0]))
    #print(list(G.neighbors(0)))
    #print([node if len(list(G.neighbors(node))) > 0 else None for node in G.nodes])

    print('All path from start to hp-m300 MAG')
    for path in nx.all_simple_paths(G, source=0, target=machine_name_list.index('Magazine HP-M300')):
        translated_path = [machine_name_list[i] for i in path]
        print(translated_path)

    edges = G.edges()
    weights = [G[u][v]['sample_count'] for u, v in edges]
    weights = [weight / max(weights) * 5 for weight in weights]
    nx.draw(G,
            pos=nx.spring_layout(G),
            labels=nx.get_node_attributes(G, 'name'),
            #nodelist=[node if len(list(G.neighbors(node))) > 0 else None for node in G.nodes],
            arrowsize=15,
            font_size=8,
            node_size=75,
            width=weights,
            edge_color='r'
            )


    plt.show()