from AntColonyOptimizer import AntColonyOptimizer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import time
import warnings
import random
import math
# 시드값 저번에 정한거
# 이찬규 : 1
# 이승열 : 2
# 임채균 : 3 
# 장지현 : 4
# 박병현 : 5
# 소준용 : 6


ad = "Data/PDP_TW (2).xlsx"
df = pd.read_excel(ad) 
df = df[["Pos1","Pos2"]]
coordinates_arr = np.array(df)


print(f'coordinates_arr : {coordinates_arr}')
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
print(dist)
optimizer = AntColonyOptimizer(ants=100, evaporation_rate=.1, intensification=2, alpha=1, beta=1,beta_evaporation_rate=0, choose_best=.1)

best = optimizer.fit(dist,100)
optimizer.plot()
