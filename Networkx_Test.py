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



    sum_of_depth_in_path = [0 for i in range(len(machine_name_list))]
    appearence_in_path = [0 for i in range(len(machine_name_list))]
    average_depth_score = [0 for i in range(len(machine_name_list))]
    rounded_average_depth_score = [0 for i in range(len(machine_name_list))]


    for end_node in nonisolated_nodes:
        for path in nx.all_simple_paths(G, source=0, target=end_node):
            for index, node_in_path in enumerate(path):
                sum_of_depth_in_path[node_in_path] += index
                appearence_in_path[node_in_path] +=1
            print([n for n in path])
            print( [G.nodes[n]['name'] for n in path])
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('##############################################################################################')

    # for end_node in end_nodes:
    #     for path in nx.all_simple_paths(G, source=0, target=end_node):
    #         for index, node_in_path in enumerate(path):
    #             sum_of_depth_in_path[node_in_path] += index
    #             appearence_in_path[node_in_path] +=1
    #         print([n for n in path])
    #         print( [G.nodes[n]['name'] for n in path])
    #     print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # print('##############################################################################################')
    #
    # left_over_machines = []
    # for i in range(len(appearence_in_path)):
    #     if appearence_in_path[i] == 0 and i not in isolated_machines:
    #         left_over_machines.append(i)
    # print('left_over_machines')
    # print(left_over_machines)
    #
    # for end_node in left_over_machines:
    #     for path in nx.all_simple_paths(G, source=0, target=end_node):
    #         for index, node_in_path in enumerate(path):
    #             sum_of_depth_in_path[node_in_path] += index
    #             appearence_in_path[node_in_path] +=1
    #         print([n for n in path])
    #         print([G.nodes[n]['name'] for n in path])
    #
    #         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # print('##############################################################################################')


    for i in range(len(sum_of_depth_in_path)):
        if appearence_in_path[i] > 0:
            rounded_average_depth_score[i] = round(sum_of_depth_in_path[i] / appearence_in_path[i])
            average_depth_score[i] = sum_of_depth_in_path[i] / appearence_in_path[i]

    print('average_depth_score')
    print(average_depth_score)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('appearence_in_path')
    print(appearence_in_path)



    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('rounded_average_depth_score')
    print(rounded_average_depth_score)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('sum_of_depth_in_path')
    print(sum_of_depth_in_path)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    depth_dict = {}
    current_dict ={}
    y_position = [7 for i in range(len(machine_name_list))]

    for i in range(len(rounded_average_depth_score)):
        if i not in isolated_nodes:
        #if average_depth_score[i] > 0:
            depth_dict[rounded_average_depth_score[i]] = depth_dict.get(rounded_average_depth_score[i], 0) + 1

    for i in range(len(rounded_average_depth_score)):
        if i not in isolated_nodes:
        #if average_depth_score[i] > 0:
            current_dict[rounded_average_depth_score[i]] = current_dict.get(rounded_average_depth_score[i], 0) + 1
            y_position[i] = current_dict[rounded_average_depth_score[i]]
    print('depth_dict')
    print(depth_dict)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    rounded_average_depth_score[0] = 0
    sum_of_depth_in_path[0] = 1
    y_position[0] = 1
    print(sum_of_depth_in_path)
    print(y_position)

    transformed_x_position = [0 for i in range(len(machine_name_list))]
    sorted_average_depth_score_index = sorted(range(len(rounded_average_depth_score)), key=lambda k: rounded_average_depth_score[k])
    for index, val in enumerate(sorted_average_depth_score_index):
        transformed_x_position[val] = index
    print('transformed_x_position')
    print(transformed_x_position)



    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    for i in range(len(machine_name_list)):
        if i in isolated_nodes == 0:
            x = -1
            y = -1
        else:
            x = rounded_average_depth_score[i]
            y = y_position[i]
            G.nodes[i]['pos'] = (x,y)

    print(G.nodes.data())

    edges = G.edges()
    weights = [G[u][v]['sample_count'] for u, v in edges]
    weights = [weight / max(weights) * 8 for weight in weights]
    nx.draw(G,
            #pos=nx.spring_layout(G),
            pos=nx.get_node_attributes(G, 'pos'),
            labels=nx.get_node_attributes(G, 'name'),
            nodelist=nonisolated_nodes,
            font_size=9,
            node_size=60,
            width=weights,
            edge_color='r'
            )
    plt.show()