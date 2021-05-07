import numpy as np
import string
import math
from python_tsp.heuristics import solve_tsp_local_search
from python_tsp.exact import solve_tsp_dynamic_programming
import time
import random
import pandas as pd
import Prob_load as Prob
import copy
from Solver2 import solve_cluster as solve
import TSP_settings as tsp
import AntColonyOptimizer


a,b,c,d = [], [], [], []
_a,_b,_c,_d = [], [], [], []

for i in range(30):
    def main():
        #Prob.generate_prob_xslx('PDP_TW.xlsx', num_task=20, num_day=1, depot_loc=[500, 500])
        day_list, tasklist, dist = copy.deepcopy(Prob.load_prob_xlsx('PDP_TW.xlsx'))
        before_time = time.time()
        solve(day_list, tasklist)
        after_time = time.time()
        #tsp.plot_schedule(day_list, tasklist, add_label=True)
        total = 0
        for _day in day_list:
            total += _day.total_distance

        total -= tsp.loc_distance([500, 500], day_list[0].route[-1].loc)
        compute = after_time - before_time
        return total, compute

    total, compute = main()
    print('ConvexHull distance : ', total)
    print('ConvexHull computation time : ', compute)

    def loc_distance(_loc1, _loc2):
        dist = math.sqrt((_loc1[0] - _loc2[0]) ** 2 + (_loc1[1] - _loc2[1]) ** 2)
        return dist


    for i in range(1):
        df = pd.read_excel('PDP_TW.xlsx')
        df = df[["Pos1", "Pos2"]]
        coordinates_arr = np.array(df)
        Pos1 = []

        for i in df['Pos1']:
            Pos1.append(i)
        Pos2 = []

        for i in df['Pos2']:
            Pos2.append(i)

        # 각좌표간의 거리를 저장한 거리배열 dist[i,j] --> 노드 i와 j 간의 거리
        dist = []
        for i in range(len(Pos1)):
            dist_list = []
            for j in range(len(Pos2)):
                dist_list.append(((Pos1[i] - Pos1[j]) ** 2 + (Pos2[i] - Pos2[j]) ** 2) ** (1 / 2))
            dist.append(dist_list)
        dist = np.array(dist, dtype='int')
        n_city = dist.shape[0]

        before_time = time.time()
        dp_permutation, dp_distance = solve_tsp_dynamic_programming(dist)
        after_time = time.time()
        print('DP distance : ', dp_distance)
        #print(f"dp__permutation : {dp_permutation}")
        print('DP computation :', after_time - before_time)

        a.append(((dp_distance - total)/total)*100)
        _a.append(((after_time - before_time - compute) / compute) * 100)
        print('(DP - ConvexHull) / ConvexHull distance \n: ',((dp_distance - total)/total)*100, '%')
        print('(DP - ConvexHull) / ConvexHull computation time \n: ', ((after_time - before_time - compute) / compute) * 100, '%')

        before_time = time.time()
        ls_permutation, ls_distance = solve_tsp_local_search(dist)
        after_time = time.time()
        print('LS_distance : ', ls_distance)
        #print(f"ls_permutation : {ls_permutation}")
        print('LS computation :', after_time - before_time)

        b.append(((ls_distance - total) / total) * 100)
        _b.append(((after_time - before_time - compute) / compute) * 100)
        print('(LS - ConvexHull) / ConvexHull \n: ',((ls_distance - total) / total) * 100, '%')
        print('(LS - ConvexHull) / ConvexHull computation time \n: ', ((after_time - before_time - compute) / compute) * 100, '%')

        def three_opt(number_of_cities, local_search_permutation, n_iter=100):

            # 노드의 수, local_search 로구한 경로, 반복횟수 입력
            # 반복횟수는 기본 100회

            n = number_of_cities
            best_dist = ls_distance
            best_permutation = local_search_permutation
            best_opt = [ls_distance, best_dist, best_permutation]
            for i in range(n_iter):
                for j in range(4):
                    a, c, e = random.sample(range(n + 1), 3)

                    a, c, e = sorted([a, c, e])
                    b, d, f = a + 1, c + 1, e + 1

                    if j == 0:
                        path_1 = local_search_permutation[:a + 1] + local_search_permutation[
                                                                    c:b - 1:-1] + local_search_permutation[
                                                                                  e:d - 1:-1] + local_search_permutation[f:]
                        dist_1 = 0
                        for i in range(1, len(path_1)):
                            dist_1 += dist[path_1[i - 1], path_1[i]]

                    elif j == 1:
                        path_2 = local_search_permutation[:a + 1] + local_search_permutation[
                                                                    d:e + 1] + local_search_permutation[
                                                                               b:c + 1] + local_search_permutation[f:]
                        dist_2 = 0
                        for i in range(len(path_2)):
                            dist_2 += dist[path_1[i - 1], path_1[i]]

                    elif j == 2:
                        path_3 = local_search_permutation[:a + 1] + local_search_permutation[
                                                                    d:e + 1] + local_search_permutation[
                                                                               c:b - 1:-1] + local_search_permutation[f:]
                        dist_3 = 0
                        for i in range(len(path_3)):
                            dist_3 += dist[path_3[i - 1], path_3[i]]

                    else:
                        path_4 = local_search_permutation[:a + 1] + local_search_permutation[
                                                                    e:d - 1:-1] + local_search_permutation[
                                                                                  b:c + 1] + local_search_permutation[f:]
                        dist_4 = 0
                        for i in range(len(path_4)):
                            dist_4 += dist[path_4[i - 1], path_4[i]]

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

        before_time = time.time()
        best = three_opt(20, ls_permutation, 100)
        after_time = time.time()
        print('3 OPT distance : ', {best[0]})
        #print(f'3 opt 최적 경로 : {best[1]}')
        print('3 OPT computation : ', after_time - before_time)

        c.append(((best[0] - total) / total) * 100)
        _c.append(((after_time - before_time - compute) / compute) * 100)
        print('(3opt - ConvexHull) / ConvexHull distance : ',((best[0] - total) / total) * 100, '%')
        print('(3opt - ConvexHull) / ConvexHull computation time \n: ',((after_time - before_time - compute) / compute) * 100, '%')


        optimizer = AntColonyOptimizer.AntColonyOptimizer(ants=100, evaporation_rate=.1, intensification=2, alpha=1, beta=1, beta_evaporation_rate=0, choose_best=0.1)

        before_time = time.time()
        best = optimizer.fit(dist, 200)
        after_time = time.time()
        print('ACO distance : ', best)
        print('ACO computation : ', after_time - before_time)
        print('(ACO - ConvexHull) / ConvexHull : ', ((best - main()) / main()) * 100, '%')
        print('(ACO - ConvexHull) / ConvexHull computation time \n: ',((after_time - before_time - compute) / compute) * 100, '%')
        d.append(((best - main()) / main()) * 100)
        _d.append(((after_time - before_time - compute) / compute) * 100)
        # optimizer.plot()

        print()



print('Result')
print('----------------------------------')
print('Dynamic Programming distance error average :', sum(a)/len(a), '%')
print('Dynamic Programming computation error average :', sum(_a)/len(_a), '%')
print('Local Search distance error average :', sum(b)/len(b), '%')
print('Local Search computation error average :', sum(_b)/len(_b), '%')
print('3OPT distance error average :', sum(c)/len(c), '%')
print('3OPT computation error average :', sum(_c)/len(_c), '%')
print('ACO distance error average :', sum(d)/len(d), '%')
print('ACO computation error average :', sum(_d)/len(_d), '%')
