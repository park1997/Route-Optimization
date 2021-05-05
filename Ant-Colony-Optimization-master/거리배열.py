import numpy as np
import pandas as pd
import sympy

np.random.seed(1)
# 시드값 저번에 정한거
# 이찬규 : 1
# 이승열 : 2
# 임채균 : 3 
# 장지현 : 4
# 박병현 : 5
# 소준용 : 6

# 행,열 갯수랑 18번째 줄에 있는 range값만 변경해주면 배열크기 변경됨
# min max 는 배열에 저장되는 거리 최소 최댓값
dist = sympy.randMatrix(r= 10 ,c = 10, min = 1, max =99, symmetric= True, seed = 0)
# sympy 의 인덱스 접근은 [r][c] 형식이 아닌 [r,c]형식로 해야함

for i in range(10):
    dist[i,i] = 0

dist = np.array(dist,dtype='float64')