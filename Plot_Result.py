import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt




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

input_data = pd.read_csv('result_plot.csv', index_col=0)
G = nx.DiGraph(input_data.values)
nx.draw(G)
plt.show()