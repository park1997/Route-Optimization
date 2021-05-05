import numpy as np
import math
import matplotlib.pyplot as plt
from python_tsp.heuristics import solve_tsp_local_search
from python_tsp.heuristics import solve_tsp_simulated_annealing
from python_tsp.exact import solve_tsp_dynamic_programming
import time
from python_tsp.exact import solve_tsp_brute_force
import random
import pandas as pd


ad = "Data/PDP_TW (2).xlsx"
print(ad)
df = pd.read_excel(ad) 
df = df[["Pos1","Pos2"]]
coordinates_arr = np.array(df)
dist = []
for i in range(coordinates_arr.shape[0]):
    arr = []
    for j in range(coordinates_arr.shape[0]):
        if i == j:
            arr.append(0)
        else:
            arr.append(math.dist(coordinates_arr[i,1:],coordinates_arr[j,1:]))
    dist.append(arr)
dist = np.array(dist,dtype = 'int')

# dp 로 구한 정확한 해 
before_time = time.time()
dp_kernel = solve_tsp_dynamic_programming(dist)
dp_distance = dp_kernel[1]
dp_permutation = dp_kernel[0]
after_time = time.time() 
print("DP")
print(f"distance : {dp_distance}")
print(f"dp_permutation : {dp_permutation}")
print('시간 :',after_time - before_time)
print()


# sa 로 구한 해 
before_time = time.time()
kernel = solve_tsp_simulated_annealing(dist)
sa_distance = kernel[1]
sa_permutation = kernel[0]
after_time = time.time() 

print("SA")
print(f"distance : {sa_distance}")
print(f"sa_permutation : {sa_permutation}")
print('시간: ',after_time - before_time)
print(f'오차 : {(sa_distance-dp_distance)/ dp_distance}')
print()


# local_Search로 구한것
before_time = time.time()
ls_permutation, ls_distance = solve_tsp_local_search(dist)
after_time = time.time()

print("LocalSearch")
print(f"distance : {ls_distance}")
print(f"ls_permutation : {ls_permutation}")
print('시간 :', after_time - before_time)
print(f'오차 : {(ls_distance-dp_distance)/ dp_distance }')

