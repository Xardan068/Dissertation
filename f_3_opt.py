# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 21:42:16 2023

@author: ZXY
"""

import tsplib95 
import networkx as nx
import pandas as pd


def calculate_tour_distance(tour, problem):
    total_distance = 0
    for i in range(len(tour)):
        v1 = tour[i]
        v1p1 = tour[(i + 1) % len(tour)]
        edge_dist = problem.get_weight(v1,v1p1)
        total_distance += edge_dist
    return total_distance
def has_duplicates(lst):
    return len(lst) != len(set(lst))


def find_worst_edge(tour, problem):
    seq_best_edge = pd.DataFrame(columns=['V1', 'V1+1', 'Distance'])
    
    for i in range(len(tour)):
        v1 = tour[i]
        v1p1 = tour[(i + 1) % len(tour)]
        edge_dist = problem.get_weight(v1, v1p1)
        new_row = pd.DataFrame([{'V1': v1, 'V1+1': v1p1, 'Distance': edge_dist}])
        seq_best_edge = pd.concat([seq_best_edge, new_row], ignore_index=True)
        
    seq_best_edge = seq_best_edge.sort_values('Distance', ascending=False).reset_index(drop=True)
    
    for i in range(len(seq_best_edge)):
        edge_start = seq_best_edge['V1'][i]
        edge_end = seq_best_edge['V1+1'][i]
        worst_edge_index = tour.index(edge_start)
        
        for j in range(len(tour)):
            if j > worst_edge_index and j != (worst_edge_index + 1) % len(tour):
                for k in range(j + 2, len(tour)):
                    if k != (worst_edge_index + 1) % len(tour) and (k + 1) % len(tour) != worst_edge_index:
                        old_dist = calculate_tour_distance(tour, problem)
                        opt = pd.DataFrame(columns=['tour', 'type', 'dis'])
                        new_row_opt = pd.DataFrame([{'tour': tour, 'type': 'O', 'dis': old_dist}])
                        opt = pd.concat([opt, new_row_opt], ignore_index=True)
                        # print("old", old_dist)
                        
                        new_tour1 = tour[:worst_edge_index+1] + tour[worst_edge_index + 1: j + 1][::-1]+tour[(j + 1) % len(tour): k + 1][::-1]+tour[k+1:]
                        new_dist1 = calculate_tour_distance(new_tour1, problem);
                        new_row1 = pd.DataFrame([{'tour': new_tour1, 'type': '1', 'dis': new_dist1}])
                        opt = pd.concat([opt, new_row1], ignore_index=True)

                                
                        new_tour2 = tour[:worst_edge_index+1]+tour[(j + 1) % len(tour): k + 1]+tour[worst_edge_index + 1: j + 1]+tour[k+1:]
                        new_dist2 = calculate_tour_distance(new_tour2, problem)
                        new_row2 = pd.DataFrame([{'tour': new_tour2, 'type': '2', 'dis': new_dist2}])
                        opt = pd.concat([opt, new_row2], ignore_index=True)
                        
                        new_tour3 = tour[:worst_edge_index+1]+tour[(j + 1) % len(tour): k + 1]+tour[worst_edge_index + 1: j + 1][::-1]+tour[k+1:]
                        new_dist3 = calculate_tour_distance(new_tour3, problem)
                        new_row3 = pd.DataFrame([{'tour': new_tour3, 'type': '3', 'dis': new_dist3}])
                        opt = pd.concat([opt, new_row3], ignore_index=True)

                        
                        new_tour4 = tour[:]+tour[(j + 1) % len(tour): k + 1][::-1]+tour[worst_edge_index + 1: j + 1]+tour[k+1:]
                        new_dist4 = calculate_tour_distance(new_tour4, problem)
                        new_row3 = pd.DataFrame([{'tour': new_tour3, 'type': '3', 'dis': new_dist3}])
                        opt = pd.concat([opt, new_row3], ignore_index=True)
                        
                        opt = opt.sort_values('dis', ascending=True).reset_index(drop=True)
                                
                        if opt['dis'][0] < old_dist and has_duplicates(opt['tour'][0])== False:
                            # print("newd", opt['dis'][0], opt['tour'][0])
                            return opt['tour'][0]
    # print("oldd", old_dist)                                              
    return tour
def three_opt(tour, problem):
    
    while True:
        new_tour= find_worst_edge(tour, problem)        
        if new_tour == tour:
            distance = sum(problem.get_weight(new_tour[i], new_tour[                
                i + 1]) for i in range(len(new_tour) - 1))
            return tour, distance
        else:
            tour = new_tour
            continue
       
# tour, distance = process(tour)
# pos = problem.display_data
# for n, p in pos.items():
#     G.nodes[n]['pos'] = p            
# G = nx.DiGraph()
# for n, p in pos.items():
#     G.add_node(n, pos=p)
# for i in range(len(tour) - 1):
#     G.add_edge(tour[i], tour[i + 1])
# pos = nx.get_node_attributes(G, 'pos')
# G.add_edge(tour[-1], tour[0])
# ####
# nx.draw(G, pos, with_labels=True, node_color='g', font_weight='bold', arrows=False)

# # 
# path_edges = [(tour[n], tour[n + 1]) for n in range(len(tour) - 1)]
# path_edges.append((tour[-1], tour[0]))
# nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, 
#                        arrowstyle='-|>', 
#                        arrowsize=10)

# plt.show() 
# end_time = time.time()
# print(f"Runtime of the code is {end_time - start_time} seconds")
# print("Best tour:", tour)
# print("Distance:", calculate_tour_distance(tour))
