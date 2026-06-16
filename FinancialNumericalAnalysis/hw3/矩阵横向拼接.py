import numpy as np
all_stockvalue=np.array([3564.0626,2943.8779,742.6273,252.1985,437.8242])
A_netprofit=np.array([2987.23,1924.35,741.65,808.19,503.30])
A_netassets=np.array([23448.83,17253.97,7053.08,5436.05,4310.01])
A=np.stack((A_netprofit,A_netassets),axis=0)
print(A)
H_netprofit=np.array([3401.2601,2191.0649,844.4427,920.2051,573.0574])
H_netassets=np.array([26698.8378,19645.3702,8030.6369,6189.4865,4703.568])
H=np.stack((H_netprofit,H_netassets),axis=0)
A_per_netprofit=A_netprofit/all_stockvalue
A_per_netassets=A_netassets/all_stockvalue
H_per_netprofit=H_netprofit/all_stockvalue
H_per_netassets=H_netassets/all_stockvalue
print("A股市场每股净收益为：",A_per_netprofit)
print("H股市场每股净收益为：",H_per_netprofit)
print("H股市场每股净资产为：",H_per_netassets)
print("A股市场每股净资产为：",A_per_netassets)
A_closeprice=np.array([5.89,3.74,6.12,35.98,6.35])
H_closeprice=np.array([5.70,3.30,5.93,38.95,5.41])

A_PB_ratio=A_closeprice/A_per_netassets
print("A股市净率为：",A_PB_ratio)
H_PB_ratio=H_closeprice/H_per_netassets
print("H股市净率为：",H_PB_ratio)

A_PE_ratio=A_closeprice/A_per_netprofit
H_PE_ratio=H_closeprice/H_per_netprofit
print("A股市盈率为：",A_PE_ratio)
print("H股市盈率为：",H_PE_ratio)

max_PB_PE=np.array([max(max(A_PB_ratio),max(H_PB_ratio)),max(max(A_PE_ratio),max(H_PE_ratio))])
print(max_PB_PE)
min_PB_PE=np.array([min(min(A_PB_ratio),min(H_PB_ratio)),min(min(A_PE_ratio),min(H_PE_ratio))])
print(min_PB_PE)

Ent_value=2e7*A_closeprice
print("E公司持有股票的市值：",Ent_value)

H_change=1e-2*np.array([-0.5263,0.3030,2.0236,1.4121,0.7394])
H_closeprice_7=H_closeprice*(1+H_change)
print("7月2日收盘价为",H_closeprice_7)