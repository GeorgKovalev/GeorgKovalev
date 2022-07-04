import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import random
from datetime import datetime
import time
from time import sleep
from stp_reader import stp_reader


dfs_nodes_order = []

def draw_graph(elist, cnt_v):
    G = nx.DiGraph() # создание графа

    nodes = [i + 1 for i in range(G.number_of_nodes())]
    G.add_weighted_edges_from(elist) # добавить список взвешенных рёбер

    labels = nx.get_edge_attributes(G, 'weight')
    # упаковка графа на плоскость. существует несколько возможных конфигураций (layout)
    random.seed(time.time())
    pos = nx.circular_layout(G)

    fig, ax = plt.subplots(figsize=(len(elist), 8))
    # список в порядке dfs

    def update(idx):
        colors_set = ["red" for i in range(cnt_v)]
        colors_set[dfs_nodes_order[idx]] = "green"
        # рендер вершин
        print(colors_set)
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
    elist, alist, node_count = stp_reader("simple.stp")

    alist += elist # don't feel difference between nodes and arcs
    # optionally: split edge to 2 arcs
    # for edge in elist:
    #     alist += edge
    #     alist += (edge[1], edge[0], edge[2])

    adj_list = [[] for i in range(node_count)]
    for arcs in alist:
        adj_list[int(arcs[0]) - 1].append(int(arcs[1]) - 1)

    start_v = 1 #int(input("Input start node!"))
    dfs(adj_list, start_v - 1)
    print(alist, node_count)
    draw_graph(alist, node_count)

def dfs(adj_list, start_v):
        stack = []
        v_colors = [0 for i in range(len(adj_list))] # in the beginning all nodes are white
        stack.append(start_v)

        while stack != []:
            cur_v = stack.pop()
            dfs_nodes_order.append(cur_v)
            for neighbour in adj_list[cur_v]:
                if v_colors[neighbour] == 0:
                    v_colors[cur_v] = 1 # grey
                    stack.append(neighbour)
            v_colors[cur_v] = 2 # black


if __name__ == "__main__":
    main()
    
