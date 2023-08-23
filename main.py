# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 09:11:18 2023

@author: ZXY
"""

import tsplib95 
import networkx as nx
import matplotlib.pyplot as plt
import time
from f_nearest_neighbour import *
from f_greedy import *
from f_2_opt import *
from f_3_opt import *
from f_cover3 import *
from f_cover4 import *

#%% Nearest neighbour

problem = tsplib95.load('dantzig42.tsp')

G = problem.get_graph()

greedy_solver = GreedyTSP(G, problem)
path, total_weight, objective_value1= greedy_solver.find_shortest_path()
plot_tour(path,problem,G)

#%% 2 opt
path, total_weight, objective_value= greedy_solver.find_shortest_path()
path_2_opt1, objective_2_opt1 = two_opt(path)
plot_tour(path_2_opt1, problem, G)


#%% 3 opt
path, total_weight, objective_value = greedy_solver.find_shortest_path()
path_3_opt1, objective_3_opt1 = three_opt(path, problem)
plot_tour(path_3_opt1, problem, G)





#%% Greedy
problem = tsplib95.load('dantzig42.tsp')

path, total_weight = greedy_shortest_path(problem)
#%% 2 opt
path, total_weight = greedy_shortest_path(problem)
path_2_opt2, objective_2_opt2 = two_opt(path)
plot_tour(path_2_opt2, problem, G)
#%% 3 opt
path, total_weight = greedy_shortest_path(problem)
path_3_opt2, objective_3_opt2 = three_opt(path, problem)
plot_tour(path_3_opt2, problem, G)



#%% Nearest insertion
problem = tsplib95.load('dantzig42.tsp')
path, total_weight = nearest_insertion(problem)
#%% 2 opt
path, total_weight = nearest_insertion(problem)
path_2_opt3, objective_2_opt3 = two_opt(path)
plot_tour(path_2_opt3, problem, G)
#%% 3 opt
path, total_weight = nearest_insertion(problem)
path_3_opt3, objective_3_opt3 = three_opt(path, problem)
plot_tour(path_3_opt3, problem, G)





#%% Cover problem 1
problem = tsplib95.load('dantzig42.tsp')
path_2_opt1, objective_2_opt1 = two_opt(path)
new_tour, total_distance, coverage_point = cover_problem(path_2_opt1, problem, D_c=20)
plot_covered_tour(new_tour, coverage_point, problem)

#%% Cover problem 1
problem = tsplib95.load('dantzig42.tsp')
path_3_opt1, objective_3_opt1 = three_opt(path, problem)
new_tour, total_distance, coverage_point = cover_problem(path_3_opt1, problem, D_c=20)
path_2_optc1, objective_2_optc1 = two_opt(new_tour)
plot_covered_tour(path_2_optc1, coverage_point, problem)


#%% Cover problem 1
problem = tsplib95.load('dantzig42.tsp')
path_3_opt1, objective_3_opt1 = three_opt(path, problem)
new_tour, total_distance, coverage_point = cover_problem(path_3_opt1, problem, D_c=20)
path_3_optc1, objective_3_optc1 = three_opt(new_tour, problem)
plot_covered_tour(path_3_optc1, coverage_point, problem)








#%% Cover problem 2
problem = tsplib95.load('dantzig42.tsp')
tour = [1, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 21, 20, 19, 18, 16, 15, 14, 13, 17, 22, 23, 12, 11, 24, 27, 26, 25, 10, 9, 8, 3, 7, 6, 5, 4, 42, 2]
path_optc2,objective_2_optc2,edges_data = cover_problem2(tour, problem, D_c = 20)
plot_tour(problem, path_optc2, edges_data)
#%% Cover problem 2 with 2-opt
problem = tsplib95.load('dantzig42.tsp')
tour = [1, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 21, 20, 19, 18, 16, 15, 14, 13, 17, 22, 23, 12, 11, 24, 27, 26, 25, 10, 9, 8, 3, 7, 6, 5, 4, 42, 2]
path_optc2,objective_2_optc2,edges_data = cover_problem2(tour, problem, D_c = 20)
path_2_optc2, objective_2_optc2 = two_opt(path_optc2)
plot_tour(problem, path_2_optc2, edges_data)
#%% Cover problem 2 with 2-opt
problem = tsplib95.load('dantzig42.tsp')
tour = [1, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 21, 20, 19, 18, 16, 15, 14, 13, 17, 22, 23, 12, 11, 24, 27, 26, 25, 10, 9, 8, 3, 7, 6, 5, 4, 42, 2]
path_optc2,objective_2_optc2,edges_data = cover_problem2(tour, problem, D_c = 20)
path_3_optc2, objective_3_optc2 = three_opt(path_optc2, problem)
plot_tour(problem, path_3_optc2, edges_data)










