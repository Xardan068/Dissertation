# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 04:01:29 2023

@author: ZXY
"""

import tsplib95 
import networkx as nx
import matplotlib.pyplot as plt
def cover_problem(tour, problem, D_c=20):
    G = problem.get_graph()

    covered_nodes = set()
    coverage_point = {}  
    covered_by = {node: [] for node in tour}  

    new_tour = tour.copy()
    multiple_covered = {} 

    for node in tour:
        if node in covered_nodes:
            new_tour.remove(node)
            continue
        for other_node in tour:
            if other_node != node and problem.get_weight(node, other_node) <= D_c:

                if other_node in coverage_point:
                    if coverage_point[other_node] != node:  
                        if other_node not in multiple_covered:
                            multiple_covered[other_node] = [coverage_point[other_node]] 
                        multiple_covered[other_node].append(node) 

                    if problem.get_weight(coverage_point[other_node], other_node) <= problem.get_weight(node, other_node):
                        continue
                covered_nodes.add(other_node)
                coverage_point[other_node] = node
                covered_by[node].append(other_node)

    for node, sources in multiple_covered.items():
        actual_source = coverage_point[node]

    new_tour_distance = 0
    for i in range(len(new_tour) - 1):
        new_tour_distance += problem.get_weight(new_tour[i], new_tour[i + 1])

    new_tour_distance += problem.get_weight(new_tour[-1], new_tour[0])

    covered_nodes_distance = 0
    for node, source in coverage_point.items():
        covered_nodes_distance += 0.5 * problem.get_weight(node, source)

    total_distance = new_tour_distance + covered_nodes_distance

    return new_tour, total_distance, coverage_point




def plot_covered_tour(new_tour, coverage_point, problem):
    G = problem.get_graph()
    
    pos = problem.display_data
    for n, p in pos.items():
        G.nodes[n]['pos'] = p

    G.add_nodes_from(G.nodes())

    for i in range(len(new_tour) - 1):
        G.add_edge(new_tour[i], new_tour[i + 1])
    G.add_edge(new_tour[-1], new_tour[0])

    nx.draw(G, pos, with_labels=True, node_color='g', edge_color='white', font_weight='bold', arrows=False)

    path_edges = [(new_tour[n], new_tour[n + 1]) for n in range(len(new_tour) - 1)]
    path_edges.append((new_tour[-1], new_tour[0]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, arrowstyle='-|>', arrowsize=10)
    
    for node, source in coverage_point.items():
        nx.draw_networkx_edges(G, pos, edgelist=[(node, source)], style='dashed', edge_color='b', arrowstyle='-')
    
    plt.show()