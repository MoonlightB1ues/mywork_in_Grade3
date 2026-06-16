import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from pandas.core.interchange.dataframe_protocol import DataFrame
from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data1=pd.read_excel("../data/hw13.2/RESSET_DRESSTK_2011_2015_1.xlsx")
data2=pd.read_excel("../data/hw13.2/RESSET_DRESSTK_2016_2020_1.xlsx")
data = pd.concat([data1, data2], axis=0)
data = data.dropna()
data = data.reset_index(drop=True) # 去除数据后对索引进行重排列
miu=np.average(data["日收益率_Dret"])
sigma=np.std(data["日收益率_Dret"])
#print(data)

dt=np.ones(len(data["日收益率_Dret"])-1)
dt[:]=10/(len(data["日收益率_Dret"]))  # 对时间取差分，单位为年,每一个dt为10年中多少份
stock_time = pd.to_datetime(data['日期_Date'][0::1], format='%Y-%M-%d')
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
table=[]
for i in range(4):   #要生成四种模拟
    epison=np.random.normal(0,1,len(dt))
    dln_p=(miu-(np.pow(sigma,2)/2))*dt+epison*sigma*np.pow(dt,1/2)
    ln_p0=np.log(45.05)
    p_hat=np.ones(len(data["日收益率_Dret"])-1)

    p_hat[0]=ln_p0
    for j in range(1,len(dln_p)):
        p_hat[j]=p_hat[j-1]+dln_p[j]
    p_hat=np.exp(p_hat)
    #取对数后得到每个时刻的lnp

    stock_time1=np.arange(0,len(p_hat),1)#这里可用来代替生成一段时间dates = pd.date_range(start="2020-01-01", end="2023-01-01", freq="D")
    ax.plot(stock_time1, p_hat,label=f"predict{i}")  #画图,标签循环
    table_true=data["收盘价(元)_Clpr"][0:len(stock_time1)]
    err=np.abs(p_hat-table_true)
    err_ratio=np.abs(p_hat-table_true)/table_true
    table1 = pd.DataFrame({
        "预测": p_hat,
        "真值": table_true,
        "误差": err,
        "误差比": err_ratio
    })   # 最好用字典的方式来创建Dataframe
    table.append(table1)   # 如何通过写循环把Dataframe 放进列表里
print(table[1])
ax.plot(stock_time1,data["收盘价(元)_Clpr"][0:len(stock_time1)],label="true")  #画出真值图
ax.legend(loc="upper right",fontsize=12)   # 用legend 最好的方式是给每条线都贴标签

fig.show()