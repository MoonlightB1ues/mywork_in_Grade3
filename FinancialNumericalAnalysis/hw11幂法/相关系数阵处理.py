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
        z1 = w/w[i_maxabsw]
        lambda1 = w[0]/z0[0]
        z0 = z1

    eigvalue = lambda1
    eigvector = z1
    return eigvalue, eigvector

data=pd.read_stata("../data/11.2.dta")

for c in list("ABCDEFGHJKLMN"):   #把每列的数据都改成数值型,原来是str型的
    data[f"{c}"] = pd.to_numeric(data[f"{c}"], errors='coerce')
data = data.drop(data.index[325])  #去掉最后一行异常数据
data.columns = data.iloc[0,:]
data = data.drop(index=0)
print(data)
# data = data.T
# print(data)
# data = data.set_columns(data.columns[0])  #把每行股票代码看做索引
# # print(data)
# data = data.T
corr_matrix = data.corr()  #协方差用data.cov()
print(corr_matrix.shape)
eigvalue, eigvector=PowerMethod_EigenValueVector(corr_matrix, 1e-5)
print(eigvalue, eigvector)