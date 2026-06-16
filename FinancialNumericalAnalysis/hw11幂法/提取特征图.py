import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigs
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

data=pd.read_csv("../data/Exp11-Python-上机数据_RankSectors.csv", sep=",")
#print(data.head())
# print(data["from_sector"].unique())
# print(len(data["to_sector"].unique()))
clo_matrix=np.zeros((len(data["from_sector"].unique()),len(data["to_sector"].unique())))  #初步构造图的维度


clos_dataframe = pd.crosstab(   #交叉表统计
    data['from_sector'],
    data['to_sector'],
    values=data['weight'],
    aggfunc='sum'
)
clos_dataframe=clos_dataframe.fillna(0)   #把Nan值替换为0
print(clos_dataframe.shape)   #此时矩阵不是n*n维的,无法进行幂法求解

#要给矩阵加五行
target_rows = list(clos_dataframe.index) + [f"add{i}" for i in range(5)]  #先给索引加五行
clos_dataframe = clos_dataframe.reindex(index=target_rows, fill_value=0)    #然后重置索引,并用0填充剩下五行
print(clos_dataframe.shape)


eigvalue,eigvector=PowerMethod_EigenValueVector(clos_dataframe,1e-5)
print(eigvector)

row_table=clos_dataframe.index  #把目标矩阵的行索引取出来
id=np.zeros(10)   #先找出特征值最大的行,索引存进ID.
for i in range(10):
    id[i]=np.argmax(eigvector)
    eigvector[int(id[i])]=0
print(id)  #此时id里面的索引是浮点数
id=id.astype(int)
print(id)
for j in id:
    print(row_table[j])

# A = clos_dataframe.values
# eigvals, eigvecs = eigs(A, k=1)
# for i in range(10):
#     id[i]=np.argmax(eigvecs)
#     eigvecs[int(id[i])]=0
# print(id)  #此时id里面的索引是浮点数
# id=id.astype(int)
# print(id)
# for j in id:
#     print(row_table[j])