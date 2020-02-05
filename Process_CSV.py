import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

sample_flow_file = 'flow.csv'
Start_Machine_Number = 989
End_Machine_Number = 1036
Total_Machine = End_Machine_Number - Start_Machine_Number + 1 + 1

def calculate_adjacency_matrix():
    Adjancency_Matrix = [[0 for i in range(Total_Machine)] for j in range(Total_Machine)]

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
                else:
                    From_Machine = From_Machine - Start_Machine_Number + 1

                To_Machine = To_Machine - Start_Machine_Number + 1
                a = Adjancency_Matrix[From_Machine][To_Machine]
                a = a + 1
                Adjancency_Matrix[From_Machine][To_Machine] = a
                line_count += 1
    return Adjancency_Matrix

if __name__ == "__main__":

    Adjancency_Matrix = calculate_adjacency_matrix()

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







    f = open("result.csv", "w+")
    a = ','.join(item for item in machine_name_list)
    a = 'Placeholder,' + a + '\n'
    f.write(a)
    #a = '\n'.join([','.join(['{:5}'.format(item) for item in row]) for row in Adjancency_Matrix])
    for i in range(Total_Machine):
        row = Adjancency_Matrix[i]
        b = ','.join(['{:5}'.format(item) for item in row])
        b = machine_name_list[i] + ',' + b + '\n'
        f.write(b)

    f.close()
    print('\n'.join([','.join(['{:5}'.format(item) for item in row]) for row in Adjancency_Matrix]))
