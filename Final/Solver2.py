import random
import TSP_settings as tsp
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import ConvexHull as CvH
import matplotlib.pyplot as plt
import math


def solve_cluster(_day_list, _tasklist):
    global insert_index
    day_list, tasklist = _day_list, _tasklist

    task_loc = list(map(lambda x: x.loc, tasklist))
    model = KMeans(n_clusters=len(day_list))
    model.fit(task_loc)
    y_predict = list(model.predict(task_loc))
    for _index in range(len(y_predict)):
        tasklist[_index].group = y_predict[_index]

    for _group in range(len(day_list)):
        group_list = list(filter(lambda x: x.group == _group, tasklist))

        loc_list = []
        for group in group_list:
            loc_list.append(group.loc)
        hull = CvH(loc_list)

        outlying = []
        for simplex in hull.vertices:
            outlying.append(loc_list[simplex])

        for _loc in outlying:
            loc_list.remove(_loc)

        for _loc in loc_list:
            min = 999999
            for _index in range(len(outlying)):
                if _index != len(outlying)-1:
                    if min >= tsp.loc_distance(outlying[_index], _loc) + \
                            tsp.loc_distance(outlying[_index+1], _loc) - \
                            tsp.loc_distance(outlying[_index], outlying[_index+1]):
                        min = tsp.loc_distance(outlying[_index], _loc) + \
                              tsp.loc_distance(outlying[_index+1], _loc) - \
                              tsp.loc_distance(outlying[_index], outlying[_index+1])
                        insert_index = _index + 1
            outlying.insert(insert_index, _loc)

        for _loc in outlying:
            for _task in group_list:
                if _loc == _task.loc:
                    day_list[_group].route.append(_task)
        start = tsp.Task()
        start.id = 0
        start.loc = [500, 500]
        end = tsp.Task()
        end.id = 0
        end.loc = [500, 500]

        day_list[_group].route.append(start)
        for _index in range(len(day_list[_group].route)):
            if _index != len(day_list[_group].route) - 1:
                day_list[_group].total_distance += tsp.distance(day_list[_group].route[_index], day_list[_group].route[_index + 1])
        day_list[_group].route.append(end)
    return day_list, tasklist
