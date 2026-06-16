import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import f
from scipy import stats
data = pd.read_csv('data/home3/RESSET_MRESSTK_1.csv')
for i in range(2, 9):
    data_read = pd.read_csv('data/home3/RESSET_MRESSTK_' + str(i) + '.csv')
    data = pd.concat((data, data_read), axis=0, ignore_index=True)
    del data_read
# print(data.columns)
data.columns = ['stk', 'date', 'close', 'tshare', 'monret', 'monrf', 'pe']    #fshare是总股,tshare是流通股
data.dropna(inplace=True)

beta=pd.read_csv('data/home3/RESSET_SMONRETBETA_BFDT12_1.csv')
for i in range(2, 8):
    data_read = pd.read_csv('data/home3/RESSET_SMONRETBETA_BFDT12_' + str(i) + '.csv')
    beta=pd.concat([beta,data_read], axis=0, ignore_index=True)  #竖着拼
    del data_read

beta.columns=["stk","date","beta"]
data=pd.merge(left=data,right=beta[["stk","date","beta"]],how='inner',on=['stk','date'])
# print(data)




data['date'] = pd.to_datetime(data['date'])
data['yearmonth'] = data['date'].dt.strftime('%Y%m').astype(int)
data['stksize'] = data['close']*data['tshare']   #流通市值等于流通股乘收盘价
data['stkep'] = 1/data['pe']   #ep是盈利价格比,pe是市盈率
data['monexcret'] = data['monret'] - data['monrf']
data.dropna(inplace = True, subset=['stksize', 'stkep'])
data=data[data['yearmonth']<=202312]
uym = np.unique(data['yearmonth'].values)
data.dropna(inplace = True)
print(uym)
print(data.columns)

gamma_me=[]
gamma_ep=[]
gamma_beta=[]

for i in uym:  #每月估计一次,回归结果存入gamma族列表
    dm=data[data['yearmonth']==i]
    x = dm.loc[:, ['stksize', 'beta', 'stkep']].values
    Y = dm.loc[:, ['monexcret']].values
    X=sm.add_constant(x)
    model = sm.OLS(Y, X)
    results = model.fit()
    params = results.params
    gamma_me.append(params[1])
    gamma_ep.append(params[3])
    gamma_beta.append(params[2])

print(gamma_me)


t_stat, p_value = stats.ttest_1samp(gamma_me, popmean=0)
print(f"me的t 统计量: {t_stat:.4f}")
print(f"p 值: {p_value:.4f}")

t_stat, p_value = stats.ttest_1samp(gamma_ep, popmean=0)
print(f"ep的t 统计量: {t_stat:.4f}")
print(f"p 值: {p_value:.4f}")

t_stat, p_value = stats.ttest_1samp(gamma_beta, popmean=0)
print(f"beta的t 统计量: {t_stat:.4f}")
print(f"p 值: {p_value:.4f}")

