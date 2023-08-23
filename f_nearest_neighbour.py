# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 20:19:39 2023

@author: ZXY
"""

import tsplib95 
import networkx as nx
import matplotlib.pyplot as plt
import time
start_time = time.time()
class GreedyTSP:
    def __init__(self, graph, problem):
        self.graph = graph
        self.problem = problem
        self.path = None
    def find_shortest_path(self):
        start = next(iter(self.graph.nodes))
        self.path = [start]
        unvisited = set(self.graph.nodes)
        unvisited.remove(start)
        
        total_weight = 0

        while unvisited:
            last_node = self.path[-1]
            next_node = min(unvisited, key=lambda node: self.graph.edges[last_node, node]['weight'])
            unvisited.remove(next_node)
            self.path.append(next_node)
        objective_value = 0
        for i in range(len(self.path) - 1):
            objective_value += self.problem.get_weight(self.path[i], self.path[i+1])
        objective_value += self.problem.get_weight(self.path[-1], self.path[0])
       
        return self.path, total_weight, objective_value

def plot_tour(path,problem,G):

    pos = problem.display_data

    for n, p in pos.items():
        G.nodes[n]['pos'] = p
    G = nx.DiGraph()
    for n, p in pos.items():
        G.add_node(n, pos=p)
    for i in range(len(path) - 1):
        G.add_edge(path[i], path[i + 1])
    pos = nx.get_node_attributes(G, 'pos')
    G.add_edge(path[-1], path[0])
    nx.draw(G, pos, with_labels=True, node_color='g', font_weight='bold', arrows=False)
    path_edges = [(path[n], path[n + 1]) for n in range(len(path) - 1)]
    path_edges.append((path[-1], path[0]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, 
                            arrowstyle='-|>', 
                                arrowsize=10)
    plt.show()
