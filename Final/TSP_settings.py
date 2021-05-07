import math
import matplotlib.pyplot as plot
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

class Day_Info:
    def __init__(self):
        self.id = 0
        self.origin = []
        self.end = []


class Day(Day_Info):
    def __init__(self):
        Day_Info.__init__(self)
        self.loc = []
        self.total_distance = 0

        self.route = []
        self.place = []


class Task_Info:
    def __init__(self):
        self.id = 0
        self.loc = []
        self.group = 'Group 0'


class Task(Task_Info):
    def __init__(self):
        Task_Info.__init__(self)
        self.done = False


class Distance_matrix:
    def __init__(self):
        self.dist = []


def distance(_vhc, _task):
    dist = math.sqrt((_vhc.loc[0] - _task.loc[0]) ** 2 + (_vhc.loc[1] - _task.loc[1]) ** 2)
    return dist


def loc_distance(_loc1, _loc2):
    dist = math.sqrt((_loc1[0] - _loc2[0]) ** 2 + (_loc1[1] - _loc2[1]) ** 2)
    return dist


def plot_schedule(vhc_list, tasklist, add_label=False, arrow_size=10):
    np.random.seed(101)
    values = range(len(vhc_list))
    jet = cm = plot.get_cmap('jet')
    cNorm = colors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    points = []
    for task in tasklist:
        points.append((task.loc[0], task.loc[1]))
        if add_label:
            plot.text(task.loc[0] - 10, task.loc[1] - 10, str(task.id) + '(Place)', fontsize=8, alpha=0.8)


    plot.scatter(500, 500, marker='s', color='blue', alpha=0.7)
    plot.scatter(list(map(lambda x: x[0], points)), list(map(lambda x: x[1], points)), marker='^', color='red',
                 alpha=0.7)


    for vhc in vhc_list:
        rng = np.random.RandomState(0)
        colorVal = scalarMap.to_rgba(values[vhc.id - 1])
        colorText = ('Vehicle ' + str(vhc.id))
        nowloc = vhc.origin
        for _task in vhc.route:
            if not _task.id == 0:
                nextone = next((task for task in tasklist if task.id == _task.id), None)
                if nextone.loc != nowloc:
                    plot.arrow(nowloc[0], nowloc[1], nextone.loc[0] - nowloc[0], nextone.loc[1] - nowloc[1],
                               length_includes_head=True, color=colorVal, label=colorText, head_width=arrow_size,
                               head_length=arrow_size,
                               alpha=0.5)
                nowloc = nextone.loc
            else:
                plot.arrow(nowloc[0], nowloc[1], 500 - nowloc[0], 500 - nowloc[1],
                           length_includes_head=True, color=colorVal, label=colorText, head_width=arrow_size,
                           head_length=arrow_size,
                           alpha=0.5)
    plot.show()