# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 21:17:53 2023

@author: ZXY
"""
import tsplib95 
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
problem = tsplib95.load('dantzig42.tsp')
G = problem.get_graph()
import time


def find_worst_edge(tour):
    seq_best_edge = pd.DataFrame(columns=['V1','V1+1','Distance'])
    
    for i in range(len(tour)):
        v1 = tour[i]
        v1p1 = tour[(i + 1) % len(tour)]
        edge_dist = problem.get_weight(v1,v1p1)
        new_row = pd.DataFrame([{'V1': v1, 'V1+1': v1p1, 'Distance': edge_dist}])
        seq_best_edge = pd.concat([seq_best_edge, new_row], ignore_index=True)

        
    seq_best_edge = seq_best_edge.sort_values('Distance', ascending=False).reset_index(drop=True)
    for idx, col in seq_best_edge.iterrows():
        edge_start = seq_best_edge['V1'][idx]
        edge_end = seq_best_edge['V1+1'][idx]
        worst_edge_index = tour.index(edge_start)
        for i in range(len(tour)):
            if i != worst_edge_index and i != (worst_edge_index + 1) % len(tour): 
                new_tour = tour[:]
#                 print(new_tour)
                
                new_tour[worst_edge_index + 1 : i + 1] = reversed(tour[worst_edge_index + 1 : i + 1])
                
                old_dist = problem.get_weight(tour[worst_edge_index], tour[(worst_edge_index + 1) % len(tour)]) \
                            + problem.get_weight(tour[i], tour[(i + 1) % len(tour)])
                new_dist = problem.get_weight(new_tour[worst_edge_index], new_tour[(worst_edge_index + 1) % len(new_tour)]) \
                            + problem.get_weight(new_tour[i], new_tour[(i + 1) % len(new_tour)])
                
                if new_dist < old_dist:
                    return new_tour
    return tour

def two_opt(tour):
    while True:
        new_tour = find_worst_edge(tour)
        if new_tour == tour:
            distance = sum(problem.get_weight(new_tour[i],new_tour[i+1]) for i in range(len(new_tour)-1))
            return tour, distance
        else:
            tour = new_tour
            continue
# new = process(tour)
# end_time = time.time()

# pos = problem.display_data
# for n, p in pos.items():
#     G.nodes[n]['pos'] = p
#     G = nx.DiGraph()
# for n, p in pos.items():
#     G.add_node(n, pos=p)
# for i in range(len(new) - 1):
#     G.add_edge(new[i], new[i + 1])
# pos = nx.get_node_attributes(G, 'pos')
# G.add_edge(new[-1], new[0])
# nx.draw(G, pos, with_labels=True, node_color='g', font_weight='bold', arrows=False)

# # 
# path_edges = [(new[n], new[n + 1]) for n in range(len(new) - 1)]
# path_edges.append((new[-1], new[0]))
# nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, 
#                        arrowstyle='-|>', 
#                        arrowsize=10)

# plt.show()
# print(f"Runtime of the code is {end_time - start_time} seconds")
# print(new)
