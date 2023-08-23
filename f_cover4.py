# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 05:15:29 2023

@author: ZXY
"""
import numpy as np
import matplotlib.pyplot as plt
import tsplib95
import networkx as nx
import pandas as pd

def cover_problem2(tour, problem, D_c = 20):

    df = pd.DataFrame({'cover point': [],
                       'set': []})

    for i in range(len(tour)):
        tour1 = tour.copy()
        tour1.pop(i)
        lst = []
        for j in range(len(tour1)):
            if problem.get_weight(tour[i],tour1[j]) <= D_c:
                lst.append(tour1[j])
        new_row = pd.Series({'cover point': tour[i], 'set': lst})
        df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

    covered_points = set()
    path = []
    cover_dict = {}

    while len(covered_points) < len(tour):
        available_rows = df[~df['cover point'].isin(covered_points)]
        if available_rows.empty:  
            break
        best_row = available_rows.loc[available_rows['set'].str.len().idxmax()]
        
        path.append(int(best_row['cover point']))

        covered_points.update(best_row['set'], {best_row['cover point']})

        cover_dict[int(best_row['cover point'])] = best_row['set']

    checked_points = {}
    duplicate_points_info = {}
    for cover_point, covered_set in cover_dict.items():
        for point in covered_set:
            if point in checked_points:
                duplicate_points_info.setdefault(point, []).append(checked_points[point])
                duplicate_points_info[point].append(cover_point)
            else:
                checked_points[point] = cover_point


    for dup_point, dup_sources in duplicate_points_info.items():
        print(f"duplicates {dup_point} appear: {dup_sources}")
    closest_points = {}
    for dup_point, dup_sources in duplicate_points_info.items():
        closest_cover_point = min(dup_sources, key=lambda x: problem.get_weight(x, dup_point))
        closest_points[dup_point] = closest_cover_point
    
    for dup_point, closest_cover_point in closest_points.items():
        for cover_point in duplicate_points_info[dup_point]:
            if cover_point != closest_cover_point and dup_point in cover_dict[cover_point]:
                cover_dict[cover_point].remove(dup_point)
    
    for point in path:
        print(f"Point {point} covers: {cover_dict[point]}")
    edges_data = [(k, v) for k, v in cover_dict.items() if v]
    
    objective_value = 0
    for i in range(len(path) - 1):
        objective_value += problem.get_weight(path[i], path[i+1])

    objective_value += problem.get_weight(path[-1], path[0])

    covered_edges = set()
    for _, row in df.iterrows():
        cover_point = int(row['cover point'])
        for point in row['set']:
            if cover_point in path:
                edge = tuple(sorted([cover_point, point]))  # To ensure (i, j) and (j, i) are treated the same
                if edge not in covered_edges:
                    objective_value += 0.5 * problem.get_weight(cover_point, point)
                    covered_edges.add(edge)

    return path, objective_value, edges_data


def plot_tour(problem, tour, edges_data):
    pos = problem.display_data

    G = nx.DiGraph()
    for n, p in pos.items():
        G.add_node(n, pos=p)
    for i in range(len(tour) - 1):
        G.add_edge(tour[i], tour[i + 1])
    pos = nx.get_node_attributes(G, 'pos')

    # Draw base graph
    nx.draw(G, pos, with_labels=True, node_color='g', font_weight='bold', arrows=False, edge_color="white")

    # Draw path edges
    path_edges = [(tour[n], tour[n + 1]) for n in range(len(tour) - 1) if tour[n] != tour[n+1]]
    path_edges.append((tour[-1], tour[0]))

    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, arrowstyle='-|>', arrowsize=10)
    for start, ends in edges_data:
        for end in ends:
            x = [pos[start][0], pos[end][0]]
            y = [pos[start][1], pos[end][1]]
            plt.plot(x, y, 'b--', linewidth=1.0)  

    plt.show()
