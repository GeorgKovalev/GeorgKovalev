import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import random
from datetime import datetime
import time
from stp_reader import stp_reader

def draw_graph():
    edges, arcs, node_count = stp_reader("b18.stp")
    elist = edges
    
    G = nx.DiGraph() 

    nodes = [i + 1 for i in range(node_count)]
    G.add_weighted_edges_from(elist)

    labels = nx.get_edge_attributes(G, 'weight')
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

if __name__ == "__main__":
    main()
