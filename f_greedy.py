# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 20:07:42 2023

@author: ZXY
"""
import tsplib95 
import networkx as nx

def greedy_shortest_path(problem):
    G = problem.get_graph()
    edges = sorted(problem.get_edges(), key=lambda edge: problem.get_weight(*edge))
    
    filtered_edges = set()
    selected_edges = []
    used_nodes = set()
    
    for edge in edges:
        if edge[0] != edge[1]:
            sorted_edge = tuple(sorted(edge))
            filtered_edges.add(sorted_edge)
    
    edges = list(filtered_edges)
    edges.sort(key=lambda edge: problem.get_weight(*edge))
    cluster = list(edges[0])
    
    for edge in edges:
        if len(cluster) == problem.dimension:
            break
    
        if edge[0] in cluster and edge[1] in cluster:
            continue
    
        if edge[0] in cluster:
            cluster.append(edge[1])
        elif edge[1] in cluster:
            cluster.append(edge[0])
    
    total_weight = sum(problem.get_weight(cluster[i], cluster[i+1]) for i in range(-1, len(cluster)-1))
    
    return cluster, total_weight
        
        
# objective_value = 0
# for i in range(len(cluster) - 1):
#     objective_value += problem.get_weight(cluster[i], cluster[i+1])
# objective_value += problem.get_weight(cluster[-1], cluster[0])
# pos = problem.display_data
# for n, p in pos.items():
#     G.nodes[n]['pos'] = p
# G = nx.DiGraph()
# for n, p in pos.items():
#     G.add_node(n, pos=p)
# for i in range(len(cluster) - 1):
#     G.add_edge(cluster[i], cluster[i + 1])
# pos = nx.get_node_attributes(G, 'pos')
# G.add_edge(cluster[-1], cluster[0])
# nx.draw(G, pos, with_labels=True, node_color='g', font_weight='bold', arrows=False)
# path_edges = [(cluster[n], cluster[n + 1]) for n in range(len(cluster) - 1)]
# path_edges.append((cluster[-1], cluster[0]))
# nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, 
#                        arrowstyle='-|>', 
#                        arrowsize=10)

# plt.show()
# end_time = time.time()
# print(cluster)
# print(f"Objective value: {objective_value}")
# print(f"Runtime of the code is {end_time - start_time} seconds")