import csv
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
sample_flow_file = 'flow.csv'
MACHINE_GROUPING_file = 'Machine_Grouping.txt'
machine_name_group_dic = {}
machine_name_group_id_dict = {}

machine_id_list = []
machine_name_list = []
machine_dict = {}
def MACHINE_GROUPING_TRANSLATION():
    machine_name_group_dic['start'] = 'start'
    with open(MACHINE_GROUPING_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if len(row) >1 :
                machine_name_group_dic[row[1]] = row[0]



def MACHINE_Name():
    with open('MachineID_MachineName.txt', mode='r') as Machine_file:
        machine_id_list.append(0)
        machine_name_list.append('start')
        machine_dict[0] = 'start'
        for line in Machine_file:
            s_line = line.split('        ')
            if len(s_line) > 1:
                machine_id = int(s_line[0])
                machine_id_list.append(machine_id)
                machine_name = s_line[1].strip()
                machine_name_list.append(machine_name)
                machine_dict[machine_id] = machine_name

def Translate_Flow():
    translated_sample_flow_file = 'translated_flow.csv'
    dup_removed_translated_sample_flow_file = 'dup_removed_translated_flow.csv'
    with open(dup_removed_translated_sample_flow_file, 'w+') as dup_removed_translated_file:
        with open(translated_sample_flow_file, 'w+') as translated_file:
            with open(sample_flow_file, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    else:
                        print(f'\t{row[0]} -- {row[1]} -- {row[2]} -- {row[3]} ')
                        From_Machine = int(row[2])
                        To_Machine = int(row[3])

                        if From_Machine == -1:
                            From_Machine = 0

                        if From_Machine in machine_dict and To_Machine in machine_dict:
                            From_Machine_Name = machine_dict[From_Machine]
                            To_Machine_Name = machine_dict[To_Machine]

                            if From_Machine_Name not in machine_name_group_dic:
                                machine_name_group_dic[From_Machine_Name] = From_Machine_Name
                            if To_Machine_Name not in machine_name_group_dic:
                                machine_name_group_dic[To_Machine_Name] = To_Machine_Name

                            if From_Machine_Name in machine_name_group_dic  and To_Machine_Name in machine_name_group_dic:
                                From_Machine_Group = machine_name_group_dic[From_Machine_Name]
                                To_Machine_Name_Group = machine_name_group_dic[To_Machine_Name]
                                print(f'\t{From_Machine_Name} -- {To_Machine_Name} -- {From_Machine_Group} -- {To_Machine_Name_Group}')
                                translated_file.write(f'\t{row[0]},{row[1]},{From_Machine_Group},{To_Machine_Name_Group}\n')
                                if From_Machine_Group != To_Machine_Name_Group:
                                    dup_removed_translated_file.write(f'\t{row[0]},{row[1]},{From_Machine_Group},{To_Machine_Name_Group}\n')

                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    machine_name_group_list = set(val for dic in machine_name_group_dic for val in machine_name_group_dic.values())
    for index, value in enumerate(machine_name_group_list):
        machine_name_group_id_dict[value] = index

def calculate_adjacency_matrix_from_translated_sample_flow(sample_flow_file):
    Total_Machine = len(machine_name_group_dic)
    Adjancency_Matrix = [[0 for i in range(Total_Machine)] for j in range(Total_Machine)]

    with open(sample_flow_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(f'\t{row[0]} -- {row[1]} -- {row[2]} -- {row[3]} ')
            From_Machine_Group = row[2]
            To_Machine_Group = row[3]

            From_Machine_id = machine_name_group_id_dict[From_Machine_Group]
            To_Machine_id = machine_name_group_id_dict[To_Machine_Group]

            a = Adjancency_Matrix[From_Machine_id][To_Machine_id]
            a = a + 1
            Adjancency_Matrix[From_Machine_id][To_Machine_id] = a
            line_count += 1
    return Adjancency_Matrix

def add_nodes_to_graph(machine_name_group_id_dict):
    for key, value in machine_name_group_id_dict.items():
        G.add_node(value,name = key)


def add_edges_to_graph(Adjancency_Matrix):
    for i in range(len(Adjancency_Matrix)):
        for j in range(len(Adjancency_Matrix)):
            if Adjancency_Matrix[i][j] > 5:
                G.add_edge(i, j, sample_count= Adjancency_Matrix[i][j])


def pos_calculation():
    isolated_nodes = list(nx.isolates(G))
    nonisolated_nodes = []
    for node in G.nodes:
        if node not in isolated_nodes:
            nonisolated_nodes.append(node)
    isolated_machines = [G.nodes[x]['name'] for x in isolated_nodes]
    print(isolated_machines)

    sum_of_depth_in_path = [0 for i in range(len(machine_name_group_id_dict))]
    appearence_in_path = [0 for i in range(len(machine_name_group_id_dict))]
    average_depth_score = [0 for i in range(len(machine_name_group_id_dict))]
    rounded_average_depth_score = [0 for i in range(len(machine_name_group_id_dict))]

    for end_node in nonisolated_nodes:
        for path in nx.all_simple_paths(G, source=machine_name_group_id_dict['start'], target=end_node):
            weight_list = []
            for n in range(len(path)-1):
                start = path[n]
                end = path[n+1]
                weight_list.append(G[start][end]['sample_count'])
            print(weight_list)
            min_weight_in_path = min(weight_list)
            print(min_weight_in_path)

            for index, node_in_path in enumerate(path):
                sum_of_depth_in_path[node_in_path] += index * min_weight_in_path
                appearence_in_path[node_in_path] += 1 * min_weight_in_path
            print([n for n in path])
            print( [G.nodes[n]['name'] for n in path])
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('##############################################################################################')

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
    y_position = [7 for i in range(len(machine_name_group_id_dict))]
    current_dict = {}
    for i in range(len(rounded_average_depth_score)):
        if i not in isolated_nodes:
            current_dict[rounded_average_depth_score[i]] = current_dict.get(rounded_average_depth_score[i], 0) + 1
            y_position[i] = current_dict[rounded_average_depth_score[i]]

    for i in range(len(machine_name_group_id_dict)):
        if i in isolated_nodes == 0:
            x = -1
            y = -1
        else:
            x = rounded_average_depth_score[i]
            y = y_position[i]
            G.nodes[i]['pos'] = (x,y)

    print(G.nodes.data())
if __name__ == "__main__":

    MACHINE_GROUPING_TRANSLATION()
    MACHINE_Name()
    Translate_Flow()
    Adjancency_Matrix = calculate_adjacency_matrix_from_translated_sample_flow('dup_removed_translated_flow.csv')
    add_nodes_to_graph(machine_name_group_id_dict)
    add_edges_to_graph(Adjancency_Matrix)
    pos_calculation()

    edges = G.edges()
    weights = [G[u][v]['sample_count'] for u, v in edges]
    weights = [weight / max(weights) * 8 for weight in weights]
    nx.draw(G,
            # pos=nx.spring_layout(G),
            pos=nx.get_node_attributes(G, 'pos'),
            labels=nx.get_node_attributes(G, 'name'),
            # nodelist=nonisolated_nodes,
            font_size=9,
            node_size=60,
            width=weights,
            edge_color='r'
            )
    plt.show()

    # print(machine_id_list)
    # print(machine_name_list)
    # print(machine_dict)
    # print(machine_name_group_dic)
    # print(machine_name_group_id_dict)

