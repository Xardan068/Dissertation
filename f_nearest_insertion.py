# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 20:45:03 2023

@author: ZXY
"""
import tsplib95
import networkx as nx

def nearest_insertion(problem):
    G = problem.get_graph()
    N = G.number_of_nodes()
    path = [1]  # 记录已访问过的节点，从1开始
    unvisited = list(range(2, N+1))  

    while unvisited:
        nearest_neighbour = min(unvisited, key=lambda x: min(G.get_edge_data(x, y)['weight'] for y in path))

        # start
        if len(path) == 1:
            path.append(nearest_neighbour)
        else:  # insert by calculating the total distance
            position = min(range(len(path) - 1), 
                           key=lambda i: G.get_edge_data(nearest_neighbour, path[i])['weight'] + 
                                         G.get_edge_data(nearest_neighbour, path[i+1])['weight'] - 
                                         G.get_edge_data(path[i], path[i+1])['weight'])

            path.insert(position + 1, nearest_neighbour)

        unvisited.remove(nearest_neighbour)
    
    total_weight = sum(G.get_edge_data(path[i], path[i+1])['weight'] for i in range(-1, len(path)-1))
    return path, total_weight