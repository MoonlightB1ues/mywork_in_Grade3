import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
from pandas.core.interchange.dataframe_protocol import DataFrame
from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def Gauss_iter(A,b,n): #A为系数矩阵,n为迭代次数
    x=np.ones(len(A))
    D=np.zeros_like(A)
    m=np.diag(A)
    for j in range(len(A)):
        D[j,j]=m[j]
    L=-1*np.tril(A,-1)
    U=-1*np.triu(A,1)
    for i in range(n):
        x=np.dot(np.linalg.inv(D-L),np.dot(U,x)+b)
        print(x)
    return x

A=np.array([3,-1,1,1,3,1,1,2,7]).reshape(3,3)
b=np.array([7,-3,11])
x=Gauss_iter(A,b,100)
print(x)