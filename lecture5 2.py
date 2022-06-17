import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import random
from datetime import datetime
import time

def read_stp(file_name : str):
    file = open(file_name, 'r')

    file_text = file.readlines()

    start_index = -1
    for i in range(len(file_text)):
        if file_text[i].startswith('SECTION Graph'):
            start_index = i
            break
    if start_index == -1:
        print("ERROR!")
        return {}

    graph = {'E': [], 'A':[], 'N': 0}
    cnt_info_lines = 0
    
    start_index += 1
    while file_text[start_index].startswith(('Nodes','Arcs', 'Edges')):
        words = file_text[start_index].split()
        if words[0] == 'Nodes':
            graph['N'] = int(words[1])
        else:
            cnt_info_lines += int(words[1])
        start_index += 1

    for i in range(cnt_info_lines):
        line = file_text[start_index + i].split()
        graph[line[0]].append((int(line[1]), int(line[2]), float(line[3])))
        
    file.close()
    return graph

def draw_graph():
    mp = read_stp("simple.stp")

    elist = mp['A'] #[(1, 2, 5.0), (2, 3, 3.0), (1, 3, 1.0), (3, 4, 7.3)]
    #for tpl in mp['E']:
        #elist.append(tpl)
        #elist.append((tpl[1], tpl[0], tpl[2]))
    
    G = nx.DiGraph() # создание графа 
    for i in range(1, mp['N']+1):
        G.add_node(i)

    nodes = [i + 1 for i in range(G.number_of_nodes())]
    G.add_weighted_edges_from(elist) # добавить список взвешенных рёбер

    labels = nx.get_edge_attributes(G, 'weight') #
    # упаковка графа на плоскость. существует несколько возможных конфигураций (layout)
    random.seed(time.time())
    seed_ = random.randint(1, 10)
    pos = nx.circular_layout(G)

    fig, ax = plt.subplots(figsize=(len(elist), 8))

    def update(idx):
        ax.clear()
        # рендер вершин
        specialNodeNumber = random.randint(1, G.number_of_nodes())
        colors_set = []
        for i in range(G.number_of_nodes()):
            colors_set.append((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors_set)
    
        # рендер рёбер
        nx.draw_networkx_edges(
            G, pos, edgelist=[elist[idx]], width=3, alpha=0.5, edge_color="r", style="dashed", ax=ax
        )

        nx.draw_networkx_edges(
            G, pos, edgelist=elist[:idx] + elist[idx + 1:], width=3, edge_color="b", ax=ax
        )

        # рендер меток вершин
        nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif", ax=ax)

        # рендер меток рёбер
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax)

        ax.set_title(f'Frame {idx}')

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(elist), interval=500, repeat=True)
    #update(1)
    plt.show()

def to_adjacency_list(edges_list : list) -> dict:
    adj_list = {}
    for edge in edges_list:
        if edge[0] not in adj_list:
            adj_list[int(edge[0])] = [(edge[1],edge[2])]
        else:
            adj_list[int(edge[0])].append( (edge[1], edge[2]) )

        if edge[1] not in adj_list:
            adj_list[int(edge[1])] = [(edge[0],edge[2])]
        else:
            adj_list[int(edge[1])].append( (edge[0], edge[2]) )

    return adj_list

def to_inc_list(edges_list : list):
    inc_list = {}
    for edge in edges_list:
        if edge[0] not in inc_list:
            inc_list[int(edge[0])] = [edge]
        else:
            inc_list[int(edge[0])].append( edge )

        if edge[1] not in inc_list:
            inc_list[int(edge[1])] = [edge]
        else:
            inc_list[int(edge[1])].append( edge )

    return inc_list
    
def main():
    draw_graph()
    '''
    a = to_inc_list([(1, 2, 5.0), (2, 3, 3.0), (1, 3, 1.0), (3, 4, 7.3)])
    for key in a.keys():
        print(f'{key}: ', end='')
        for i in a[key]:
            print(i, end = '\t')
        print()'''

if __name__ == "__main__":
    main()
