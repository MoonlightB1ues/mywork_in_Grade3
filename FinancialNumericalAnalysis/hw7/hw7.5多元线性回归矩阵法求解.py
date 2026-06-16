import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data=pd.read_excel("../data/hw7.5.xlsx")
print(data.head())
def myfun_LSQ(Xi,Yi):
    ParLSQ=(np.dot(np.dot(np.linalg.inv(np.dot(Xi.T,Xi)),Xi.T),Yi))
    return ParLSQ

matrix = data.values
Yi = np.log(matrix[:,0])     #Yi是n*1矩阵 Yi值的解释变量
matrix[:,0]=1                #matrix是n,k+1维矩阵,第一列全为1,后面n*k是解释变量的值
matrix[:,1]=np.log(matrix[:,1])


print(matrix)


print(Yi.shape,matrix.shape)
beta=myfun_LSQ(matrix,Yi)    #返回系数矩阵,第一项是常数项
print(beta)
b=beta[0]  #常数项的值
k=beta[1:-1]  #各解释变量的系数的值
