# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 21:50:50 2023

@author: ZXY
"""

import numpy as np
rnd = np.random
from docplex.mp.model import Model
import tsplib95
import warnings
warnings.filterwarnings("ignore", category=Warning)
problem = tsplib95.load('dantzig42.tsp')
G = problem.get_graph()
n = 42
V = range(1,n+1)
A = [(i,j) for i in V for j in V if i!=j]
D_c = 20
# loc = problem.display_data
c={}
for i in range (len(A)):
    c[A[i]] = problem.get_weight(A[i][0],A[i][1])
    
a = {}
for i in range(len(A)):
    if c[A[i]] < D_c:
        a[A[i]] = 1
    else:
        a[A[i]] = 0
for i in V:
    a[i,i] = 1


# Model
mdl = Model("TSP")

# Decision variables
keys_x = [(i,j) for (i,j) in A]
keys_u = [(i,j) for i in V for j in V if  a[i,j]==1]
#define a new v as u[i]
keys_v = [i for i in V]
x = mdl.binary_var_dict(keys_x, name = 'x')
u = mdl.binary_var_dict(keys_u, name = 'u')
v = mdl.continuous_var_dict(keys_v, lb = 0, name = 'v')
#parameter a

mdl.parameters.timelimit=60


# Objective function
mdl.minimize(mdl.sum(x[i,j]*c[i,j]for (i,j) in A) +mdl.sum(0.5*c[i,j]*u[i,j]  for (i,j) in A if a[i,j]==1))


# Constraints
mdl.add_constraints(mdl.sum(x[i,j] for j in V if i!=j) == u[i,i] for i in V)
mdl.add_constraints(mdl.sum(x[j,i] for j in V if i!=j) == u[i,i] for i in V)



#City i can cover city j only if the distance is less than or equal to 50 and a[i, j] is 1
mdl.add_constraints(mdl.sum(u[i, j]*a[i,j] for i in V if a[i,j] ==1) == 1 for j in V)
mdl.add_constraints(u[i, i] >= u[i,j] for i in V for j in V if  a[i,j]==1)

u[0,0] = 0

mdl.add_constraints(v[i]-v[j] + n*x[i,j] <= n-1 for i in range(2,n+1) for j in range(2,n+1) if i!=j)





# Solve and print output
solution = mdl.solve(log_output = True)
print(solution)
