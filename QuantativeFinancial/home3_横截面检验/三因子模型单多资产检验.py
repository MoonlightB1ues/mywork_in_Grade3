import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import f

data_factors = pd.read_csv('data/home2/RESSET_THRFACDAT_WEEKLY_1.csv')
data_factors.columns = ["exc",'date', 'mkt', 'smb', 'hml']
data_factors['date'] = pd.to_datetime(data_factors['date'])
data_factors['yearmonth'] = data_factors['date']
data_factors.drop_duplicates(subset=['date'], inplace=True)
print(data_factors)
#清洗因子数据

data_index = pd.read_csv('data/home2/RESSET_IDXWKRET_1.csv')
data_index.columns = ['idxname', 'date', 'return']
data_index['date'] = pd.to_datetime(data_index['date'])
data_index['yearmonth'] = data_index['date']
print(data_index)
#导入指数数据

idxname = np.unique(data_index['idxname'].values)
print(idxname)
data_xinxi = data_index[data_index['idxname'] == idxname[0]]
data_gongyong = data_index[data_index['idxname'] == idxname[1]]
data_yiyao = data_index[data_index['idxname'] == idxname[2]]
data_cailiao = data_index[data_index['idxname'] == idxname[3]]
data_xiaofei = data_index[data_index['idxname'] == idxname[4]]
data_nengyuan = data_index[data_index['idxname'] == idxname[5]]
data_jinrong = data_index[data_index['idxname'] == idxname[6]]
print(data_xinxi.shape)

data_rf = pd.read_csv('data/home2/RESSET_WKRET_1.csv')
data_rf.columns = ['date', 'rfreturn']
data_rf['date'] = pd.to_datetime(data_rf['date'])
data_rf['yearmonth'] = data_rf['date']
print(data_rf.shape)
print(data_rf.head())
#导入无风险收益

data_matrix = pd.merge(left=data_factors[['yearmonth', 'date', 'mkt', 'smb', 'hml']],
                      right=data_xinxi[['yearmonth', 'return']],
                      on=['yearmonth'],
                      how='inner')

data_matrix = pd.merge(left=data_matrix,
                      right=data_gongyong[['yearmonth', 'return']],
                      on=['yearmonth'],
                      how='inner',
                      suffixes=['', '_gy'])

data_matrix = pd.merge(left=data_matrix,
                      right=data_yiyao[['yearmonth', 'return']],
                      on=['yearmonth'],
                      how='inner',
                      suffixes=['', '_yy'])

data_matrix = pd.merge(left=data_matrix,
                      right=data_cailiao[['yearmonth', 'return']],
                      on=['yearmonth'],
                      how='inner',
                      suffixes=['', '_cl'])

data_matrix = pd.merge(left=data_matrix,
                      right=data_xiaofei[['yearmonth', 'return']],
                      on=['yearmonth'],
                      how='inner',
                      suffixes=['', '_xf'])
#
data_matrix = pd.merge(left=data_matrix,
                      right=data_nengyuan[['yearmonth', 'return']],
                      on=['yearmonth'],
                      how='inner',
                      suffixes=['', '_ny'])

data_matrix = pd.merge(left=data_matrix,
                      right=data_jinrong[['yearmonth', 'return']],
                      on=['yearmonth'],
                      how='inner',
                      suffixes=['', '_jr'])

data_matrix = pd.merge(left=data_matrix,
                      right=data_rf[['yearmonth', 'rfreturn']],
                      on=['yearmonth'],
                      how='inner')
#横着把数据拼起来
print(data_matrix.shape)

data_matrix.columns = ['yearmonth', 'date', 'mkt', 'smb', 'hml', 'xinxi', 'gongyong', 'yiyao',
                        'cailiao', 'xiaofei', 'nengyuan', 'jinrong', 'rfreturn']

data_matrix.dropna(inplace=True)
data_matrix.sort_values(by='date', inplace=True) #按时间顺序排序

print(data_matrix)

x = data_matrix.loc[:, ['mkt', 'smb', 'hml']].values
ret_rf = data_matrix.loc[:, ['rfreturn']].values
ret_stock = data_matrix.loc[:, ['jinrong']].values


# 单资产检验
X = sm.add_constant(x)
Y = ret_stock - ret_rf
model = sm.OLS(Y, X)
results = model.fit()
print(results.summary())


T = len(Y)
N = 10
K = 3
y = data_matrix.iloc[:, 5:15].values - data_matrix.loc[:, ['rfreturn']].values
x = data_matrix.loc[:, ['mkt', 'smb', 'hml']].values  #只要把x,y定义好就行,后续的检验复制粘贴
x = sm.add_constant(x)
xTx = np.dot(np.transpose(x), x)
xTy = np.dot(np.transpose(x), y)
AB_hat = np.dot(np.linalg.inv(xTx), xTy)
ALPHA = AB_hat[0]


RESD = y - np.dot(x, AB_hat)
COV = np.dot(np.transpose(RESD), RESD)/T
invCOV = np.linalg.pinv(COV)


fs = x[:, [1, 2, 3]]
muhat = np.mean(fs, axis=0).reshape((3, 1))
fs = fs - np.mean(fs, axis=0)
omegahat = np.dot(np.transpose(fs), fs)/T
invOMG = np.linalg.pinv(omegahat)

xxx = np.dot(np.dot(np.transpose(muhat), invOMG), muhat)
yyy = np.dot(np.dot(ALPHA, invCOV), np.transpose(ALPHA))
GRS = (T-N-K)/N*(1/(1+xxx))*yyy
pvalue = 1 - f.cdf(GRS[0][0], N, T-N-K)

print('三因子模型的多资产检验结果')
print('{:>7s},{:>7s},{:>7s},{:>7s},{:>7s},{:>7s},{:>7s},{:>7s},{:>7s}'.format('alpha1', 'alpha2', 'alpha3', 'alpha4', 'alpha5', 'alpha6', 'alpha7', 'GRS', 'pvalue'))
print('{:7.4f},{:7.4f},{:7.4f},{:7.4f},{:7.4f},{:7.4f},{:7.4f},{:7.4f},{:7.4f}'.format(ALPHA[0], ALPHA[1], ALPHA[2], ALPHA[3], ALPHA[4], ALPHA[5], ALPHA[6], GRS[0][0], pvalue))