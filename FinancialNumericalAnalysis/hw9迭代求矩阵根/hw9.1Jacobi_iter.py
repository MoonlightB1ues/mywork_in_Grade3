import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from pandas.core.interchange.dataframe_protocol import DataFrame
from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def Jacobi_iter(A,b,n):   #雅各比迭代, A是系数矩阵,b是方程右边的值,n为迭代次数
    x=np.ones(len(A))
    D=np.zeros((len(A[0]),len(A)))
    m=np.diag(A)
    for j in range(len(A)):
        D[j,j]=m[j]
    for i in range(n):
        x=np.dot(np.linalg.inv(D),np.dot((D-A),x)+b)
        print(x)
    return x

A=np.array([3,-1,1,1,3,1,1,2,7]).reshape(3,3)
b=np.array([7,-3,11])
D=np.diag(A)
x=Jacobi_iter(A,b,100)
print(x)