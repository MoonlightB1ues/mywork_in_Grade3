import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import statsmodels.api as sm
from matplotlib import pyplot as plt


bond_data=pd.read_excel("../data/债券数据.xlsx")


bond_data.columns=["number","name","date","f","r","netp"]
print(bond_data.head())
bond_data["date"]=pd.to_datetime(bond_data["date"],format="%Y-%m-%d")
ctd = pd.DataFrame([[1,"CTD","2032-12-25",1,1.66,100.0695]], columns=["number", "name", "date", "f", "r", "netp"])
ctd["date"]=pd.to_datetime(ctd["date"],format="%Y-%m-%d")
bond_data=pd.concat([ctd,bond_data],axis=0,ignore_index=True)

now_time=pd.to_datetime("2026-4-14",format="%Y-%m-%d")
D_now_time=pd.to_datetime("2026-5-14",format="%Y-%m-%d")
def caculate_bond_tenor(nowtime,overtime,f):  #计算付息时点的时长  思路是算出总间隔,取整,根据频率生成等比数列,总间隔减去新生成数列即为对应时间点
    full_time=(overtime-nowtime).dt.days/365.0
    cash_flow_tenors = []
    for t, f in zip(full_time, f):
        step = 1.0 / f  # 每次付息的年化间隔
        # 计算剩余付息次数 (向下取整)
        # 加上一个极小值(1e-9)防止浮点精度导致正好卡在整数时少算一期
        num_periods = int(np.floor(t * f + 1e-9))   #因为这里是向下取整了,所以算tenors的时候periods要加一
        # 生成期限序列：从当前到期日，按 step 倒推，并翻转顺序(从小到大)
        tenors = t - np.arange(num_periods+1) * step
        tenors = tenors[::-1]  # 翻转，让离现在最近的排在前面
        cash_flow_tenors.append(tenors)
    return cash_flow_tenors

cash_flow_tenors=caculate_bond_tenor(now_time,bond_data["date"],bond_data["f"])
D_cash_flow_tenors=caculate_bond_tenor(D_now_time,bond_data["date"],bond_data["f"])
full_price_series=[]
for i, tenors in enumerate(cash_flow_tenors):
    print(f"债券 {i + 1} 现金流时点 (年): {tenors}")
    full_price=bond_data.iloc[i,-1]+bond_data.iloc[i,-2]*(1-tenors[0])
    full_price_series.append(full_price)1
full_price_dataframe=pd.DataFrame(full_price_series,columns=["fulp"])
bond_data=pd.concat([bond_data,full_price_dataframe],axis=1)
print(bond_data)


def equation(irr, p, r, tenors):
    f = p - np.sum(r / (np.exp(irr)*tenors)) - 100 / (np.exp(irr*tenors[-1]))  #定义目标函数f(x)
    return f

def duration(res,p,r,tenors):
    f= (np.sum(r / (np.exp(res)*tenors)*tenors)+100 / (np.exp(res*tenors[-1]))*tenors[-1])/p
    return f
IRR=[]
D_series=[]
for p,r,tenors,D_tenors in zip(bond_data["fulp"],bond_data["r"],cash_flow_tenors,D_cash_flow_tenors):
    res = fsolve(equation, x0=0.05, args=(p, r, tenors))
    D_bond=duration(res,p,r,D_tenors)
    IRR.append(res[0])
    D_series.append(D_bond)
print(IRR,D_series)
D_series = [x[0] for x in D_series]
IRR_D=pd.DataFrame({"IRR":IRR,"D_series":D_series})
bond_data=pd.concat([bond_data,IRR_D],axis=1)

print(bond_data)

V_H=np.sum(bond_data.loc[1:6,"fulp"])*1e5
w=bond_data.loc[1:6,"fulp"]/np.sum(bond_data.loc[1:6,"fulp"])
D_H=np.dot(w,bond_data.loc[1:6,"D_series"])
print(D_H)
D_G=bond_data.loc[0,"D_series"]
V_G=108.505*1e4
N=D_H*V_H/D_G/V_G
print(N)