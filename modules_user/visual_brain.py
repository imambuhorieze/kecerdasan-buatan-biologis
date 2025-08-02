# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import matplotlib.pyplot as plt
import networkx as nx

def visualize_brain(path_history):
    G = nx.DiGraph()
    for path in path_history:
        for i in range(len(path)-1):
            G.add_edge(path[i], path[i+1])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=3000, font_size=10, font_weight="bold")
    plt.title("Visualisasi Jalur Otak Mimi")
    plt.show()
