import numpy as np
import string
import math
from python_tsp.heuristics import solve_tsp_local_search
import time
import random
import pandas as pd



for i in range(6):
    ad = "Data/PDP_TW ({}).xlsx".format(i)
    df = pd.read_excel(ad) 
    df = df[["Pos1","Pos2"]]
    coordinates_arr = np.array(df)
    
    # 각좌표간의 거리를 저장한 거리배열 dist[i,j] --> 노드 i와 j 간의 거리
    dist = []
    for i in range(coordinates_arr.shape[0]):
        arr = []
        for j in range(coordinates_arr.shape[0]):
            if i >= j:
                arr.append(0)
            else:
                arr.append(math.dist(coordinates_arr[i,1:],coordinates_arr[j,1:]))
        dist.append(arr)
    dist = np.array(dist,dtype = 'int')
    n_city = dist.shape[0]

    before_time = time.time()
    ls_permutation, ls_distance = solve_tsp_local_search(dist)
    after_time = time.time()
    print(f"distance : {ls_distance}")
    print(f"ls_permutation : {ls_permutation}")
    print('localsearch 시간 :', after_time - before_time)

    def three_opt(number_of_cities,local_search_permutation,n_iter = 100):

        # 노드의 수, local_search 로구한 경로, 반복횟수 입력
        # 반복횟수는 기본 100회
        
        n = number_of_cities
        best_dist = ls_distance
        best_permutation = local_search_permutation
        best_opt = [ls_distance,best_dist,best_permutation]
        for i in range(n_iter):
            for j in range(4):
                a, c, e = random.sample(range(n+1), 3)

                a, c, e = sorted([a, c, e])
                b, d, f = a+1, c+1, e+1

                if j == 0:
                    path_1 = local_search_permutation[:a+1] + local_search_permutation[c:b-1:-1] + local_search_permutation[e:d-1:-1] + local_search_permutation[f:] 
                    dist_1 = 0
                    for i in range(1,len(path_1)):
                        dist_1 += dist[path_1[i-1],path_1[i]]

                elif j == 1:
                    path_2 = local_search_permutation[:a+1] + local_search_permutation[d:e+1] + local_search_permutation[b:c+1]    + local_search_permutation[f:] 
                    dist_2 = 0
                    for i in range(len(path_2)):
                        dist_2 += dist[path_1[i-1],path_1[i]]

                elif j == 2:
                    path_3 = local_search_permutation[:a+1] + local_search_permutation[d:e+1] + local_search_permutation[c:b-1:-1] + local_search_permutation[f:] 
                    dist_3 = 0
                    for i in range(len(path_3)):
                        dist_3 += dist[path_3[i-1],path_3[i]]

                else:
                    path_4 = local_search_permutation[:a+1] + local_search_permutation[e:d-1:-1] + local_search_permutation[b:c+1] + local_search_permutation[f:] 
                    dist_4 = 0
                    for i in range(len(path_4)):
                        dist_4 += dist[path_4[i-1],path_4[i]]

            min_dist = min(dist_1, dist_2, dist_3, dist_4)
            

            if min_dist == dist_1:
                min_permutation = path_1
            elif min_dist == dist_2:
                min_permutation = path_2
            elif min_dist == dist_3:
                min_permutation = path_3
            else:
                min_permutation = path_4

            if min_dist < best_dist:
                
                best_dist = min_dist
                best_opt[0] = best_dist
                best_opt[1] = min_permutation

            
        
        return best_opt

    best = three_opt(20,ls_permutation,100)
    print(f'3 opt 최적 거리 : {best[0]}')
    print(f'3 opt 최적 경로 : {best[1]}')
    print(f'시간 : {time.time()-before_time}')

    print()
    print()
    