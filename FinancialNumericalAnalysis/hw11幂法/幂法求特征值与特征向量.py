import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def PowerMethod_EigenValueVector(A, E):
    n = len(A)
    z0 = np.random.random((n,1))
    lambda0 = 0.9
    lambda1 = 1.0
    while abs(lambda1 - lambda0) > E:
        lambda0 = lambda1
        w = np.dot(A, z0)
        absw = abs(w)
        i_maxabsw = np.argmax(absw)
        z1 = w/w[i_maxabsw]  #归一化
        lambda1 = w[0]/z0[0]
        z0 = z1
        # print(lambda1)   输出每次迭代结果
        # print(z1)
    eigvalue = lambda1
    eigvector = z1
    return eigvalue, eigvector

A=np.array([[3,-4,3,-4,6,3,3,10,1]]).reshape(3,3)
eigvalue, eigvector=PowerMethod_EigenValueVector(A, 1e-5)
print(eigvalue)
print(eigvector)