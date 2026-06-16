import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from envs.my_pythorch.Lib.pydoc import describe
from pandas.core.interchange.dataframe_protocol import DataFrame


plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data=pd.read_csv("../data/Exp08-Python-实验数据-LPPLS模型估参.csv", sep=",", encoding='GB2312')
print(data.columns)
data.columns = data.columns.str.strip()
print(data.columns)
data["时间"] = pd.to_datetime(data["时间"].str.strip(), format="%Y/%m/%d")
base_date = pd.to_datetime("2016/01/01", format="%Y/%m/%d")
data["时间差（天数）"] = (data["时间"] - base_date).dt.days
print(data.head())
base=data["时间差（天数）"].to_numpy()
x1=np.pow(base,0.2932)
x2=x1*np.cos(6.1023*np.log(base))
x3=x1*np.sin(6.1023*np.log(base))
onee=np.ones_like(x1)
X=np.vstack((onee,x1,x2,x3)).T
print(X)
Y=data["收盘"].to_numpy().reshape(len(x1),1)
Y=np.log(Y)
def myfun_LSQ(Xi,Yi):
    ParLSQ=(np.dot(np.dot(np.linalg.inv(np.dot(Xi.T,Xi)),Xi.T),Yi))
    return ParLSQ
print(X.shape,Y.shape) #矩阵对不齐就把形状掏出来看看
beta=myfun_LSQ(X,Y)
print(myfun_LSQ(X,Y))
Yhat=X@beta
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(base,Y)
ax.plot(base,Yhat)
plt.show()