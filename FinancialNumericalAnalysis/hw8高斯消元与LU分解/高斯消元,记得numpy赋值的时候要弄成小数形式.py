import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from envs.my_pythorch.Lib.pydoc import describe
from pandas.core.interchange.dataframe_protocol import DataFrame


plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
def pivot_choose(AU,k):
    B=AU[k:,k:]
    imb=np.argmax(np.abs(B[:,0])) #找到最大行
    if imb!=0:   #交换行
        B1=B[0,:].copy()
        B[0,:]=B[imb,:]
        B[imb,:]=B1
    AU[k:,k:]=B   #接到原矩阵
    return AU


def GE(AU,k):   #高斯消元
    rowk=AU[k,:]
    matrix_underk=AU[k+1:,:]
    for i in range(len(matrix_underk[:,0])):
        mk=matrix_underk[i,k]/rowk[k]
        matrix_underk[i,:]=matrix_underk[i,:]-mk*rowk
    AU[k+1:,:]=matrix_underk
    return AU

def BI(U,g,n):     # 求解出每个x的值,并以列表存储
    x=np.zeros([n,1])
    x[n-1]=g[n-1]/U[n-1,n-1]
    for i in range(n-2,-1,-1):
        x[i]=(g[i]-np.dot(U[i,i+1:],x[i+1:]))/U[i,i]
    root=x
    return root

def PPGE(A,b):    #综合用法
    AU=np.concatenate((A,b),axis=1)
    n=len(AU[:,0])
    k=0
    while k<n:
        AU=pivot_choose(AU,k)
        AU=GE(AU,k)
        k=k+1
    U=AU[:,0:n]
    g=AU[:,n]
    root=BI(U,g,n)
    print(U)
    return root

A=np.array([2.0,1,-1,2,4,4,1,3,-6,-1,10,10,-2,1,8,4],dtype=float).reshape(4,4)
b=np.array([2,4,-5,1]).reshape(4,1)
root=PPGE(A,b)
print(root)