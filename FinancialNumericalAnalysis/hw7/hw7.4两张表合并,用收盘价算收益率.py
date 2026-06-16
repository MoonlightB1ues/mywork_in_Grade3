import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data300=pd.read_excel('D:\pythonwork\data\hw7.4_000300.xlsx')
data002=pd.read_excel('D:\pythonwork\data\hw7.4_000002.xlsx')
# print(data002)
# print(data300)
data300["交易日期_TrdDt"]=pd.to_datetime(data300["交易日期_TrdDt"],format='%Y-%m-%d')
data002["日期_Date"]=pd.to_datetime(data002["日期_Date"],format='%Y-%m-%d')
#print(data002)
data300.rename(columns={"交易日期_TrdDt": "日期_Date"}, inplace=True)

data=pd.merge(data300,data002,on="日期_Date")   #合并两张表


data = data.dropna()  #去除Nan
data = data.reset_index(drop=True)
print(data.columns)
yiled=(data["收盘价(元)_Clpr"]-data["收盘价(元)_Clpr"].shift(1))/data["收盘价(元)_Clpr"].shift(1)  #通过收盘价计算收益率的方式
def myfun_LSQ(Xi, Yi):
    n = len(Xi)
    sumXi = np.sum(Xi)
    sumXi2 = np.sum(Xi**2)
    sumYi = np.sum(Yi)
    sumXiYi = np.sum(Xi*Yi)
    A = np.array([[n, sumXi], [sumXi, sumXi2]])
    b = np.array([[sumYi], [sumXiYi]])
    ParLSQ = np.dot(np.linalg.inv(A), b)
    return ParLSQ
Xi = data["日收益率_Dret"]
Yi = data["指数日收益率_IdxDRet"]
ParLSQ = myfun_LSQ(Xi, Yi)
b = ParLSQ[0]
m = ParLSQ[1]
x = data["日收益率_Dret"]
y = m*x+b
plt.plot(Xi, Yi, 'ro',markersize=2)
plt.plot(x, y, 'b-', lw=2)
plt.show()