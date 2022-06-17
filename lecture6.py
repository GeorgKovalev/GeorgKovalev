import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import random
from datetime import datetime
import time
from time import sleep

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

dfs_nodes_order = []

def draw_graph(elist, cnt_v):
    G = nx.DiGraph() # создание графа
    for i in range(1, cnt_v):
        G.add_node(i)

    nodes = [i + 1 for i in range(G.number_of_nodes())]
    G.add_weighted_edges_from(elist) # добавить список взвешенных рёбер

    labels = nx.get_edge_attributes(G, 'weight') #
    # упаковка графа на плоскость. существует несколько возможных конфигураций (layout)
    random.seed(time.time())
    pos = nx.circular_layout(G)

    fig, ax = plt.subplots(figsize=(len(elist), 8))
    # список в порядке dfs
    
    def update(idx):
        ax.clear()
        # рендер вершин
        colors_set = []
        for i in range(cnt_v):
            colors_set.append( (1, 0, 0) )
        colors_set[dfs_nodes_order[idx]] = (0, 1, 0)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors_set)
    
        # рендер рёбер
        nx.draw_networkx_edges(
            G, pos, edgelist=elist, width=3, edge_color="b", ax=ax
        )

        # рендер меток вершин
        nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif", ax=ax)

        # рендер меток рёбер
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax)

        ax.set_title(f'Frame {idx}')

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(dfs_nodes_order), interval=1000, repeat=False)
    plt.show()

def main():
    mp = read_stp("simple.stp")
    using_character = 'A'
    other_character = 'E'
    
    elist = mp[using_character] + mp[other_character]
    adj_list = [[] for i in range(mp['N'])]
    for edges in mp[using_character]:
        adj_list[edges[0] - 1].append(edges[1] - 1)

    visited = [False] * mp['N']
    start_v = 1 #int(input("Input start node!"))
    dfs(adj_list, visited, start_v - 1)
    draw_graph(elist, mp['N'])

def dfs(adj_list, visited, cur_v):
        if visited[cur_v] == True:
            return

        visited[cur_v] = True
        dfs_nodes_order.append(cur_v)
        for neighbour in adj_list[cur_v]:
            dfs(adj_list, visited, neighbour)

if __name__ == "__main__":
    main()
    
