import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('ssec_daily.csv', encoding='GB2312', usecols=[2, 6])
data.columns = ['date', 'close']
p = data['close'].values
r = np.log(p[1:]) - np.log(p[:-1])
from arch import arch_model   #引用类方法
# 拟合GARCH(1, 1)模型，均值为常数，冲击为正态分布
am_garch = arch_model(r*100, mean='constant', vol='garch', p=1, q=1, dist='normal') #定义类
res_garch = am_garch.fit()
print(res_garch.summary())

# 拟合GARCH(1, 1)模型，均值过程为AR(1)，冲击为正态分布
am_garch = arch_model(r*100, mean='ar',lags=1, vol='garch', p=1, q=1, dist='normal')   #mean='ar'是反映在\mu=u_t+\episilon上,认为u是上n期(n由lag决定)的线性拟合
res_ar_garch = am_garch.fit()
print(res_ar_garch.summary())
#拟合EGARCH(1, 1)模型，均值为常数，冲击为正态分布
am_egarch = arch_model(r*100, mean='constant', vol='egarch', p=1, o=1, q=1, dist='normal')
res_am_egarch = am_egarch.fit()
print(res_am_egarch.summary())

#用拟合出来的数据画图
sim_garch = arch_model(None, mean='constant', vol='garch', p=1, q=1, dist='normal')
sim_garch_data = sim_garch.simulate(res_garch.params, 1000)
print(sim_garch_data)
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# ax.plot(sim_garch_data["data"]/100,".")
# ax.plot(r[0:1000],".")
ax.plot(r[0:1000]-sim_garch_data["data"]/100,".")
fig.show()