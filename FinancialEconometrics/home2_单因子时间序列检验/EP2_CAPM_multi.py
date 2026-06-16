import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import chi2, f
import warnings
warnings.filterwarnings("ignore")

stock_data1 = pd.read_csv('../data/1EShowData_data_5stocks_daily_price_2001-2010.csv',
                          encoding='GB2312',
                          usecols=[0, 1, 5, 10])
stock_data2 = pd.read_csv('../data/1EShowData_data_5stocks_daily_price_2011-2015.csv',
                          encoding='GB2312',
                          usecols=[0, 1, 5, 10])
stock_data3 = pd.read_csv('../data/1EShowData_data_5stocks_daily_price_2016-2018.csv',
                          encoding='GB2312',
                          usecols=[0, 1, 5, 10])
stock_data = pd.concat([stock_data1, stock_data2,stock_data3], ignore_index=True)   #将三支股票竖着并在一起


stock_data.columns = ['code', 'date', 'close', 'rfreturn']
stock_data.dropna(inplace=True)
stock_data.sort_values(by='code', inplace=True)
stk_codes = np.unique(stock_data['code'].values)  #总共五支股票
print(stock_data.head())

stock_data50 = stock_data[stock_data['code'] == stk_codes[0]].copy() #取单个股票
stock_data50['date'] = pd.to_datetime(stock_data50['date'])

stock_data50.sort_values(by=['date'], inplace=True)  #对数收益率
stock_data50['return'] = np.log(stock_data50['close']) - np.log(stock_data50['close'].shift(periods=1))
stock_data50.dropna(inplace=True)

ind = (stock_data50['return'] >= -0.1) & (stock_data50['return'] <= 0.1)  #去除极端值
stock_data50 = stock_data50.loc[ind, :]

fig1=plt.figure()
ax1=fig1.add_axes((0.2,0.2,0.7,0.7))
ax1.plot(stock_data50['return'].values)


stock_data51 = stock_data[stock_data['code'] == stk_codes[1]]   #对第二只股票进行相同操作,应该是蒋志强的代码,不写循环
stock_data51['date'] = pd.to_datetime(stock_data51['date'])
stock_data51.sort_values(by=['date'], inplace=True)
stock_data51['return'] = np.log(stock_data51['close']) - np.log(stock_data51['close'].shift(periods=1))
stock_data51.dropna(inplace=True)
ind = (stock_data51['return'] >= -0.1) & (stock_data51['return'] <= 0.1)
stock_data51 = stock_data51.loc[ind, :]

fig2=plt.figure()
ax2=fig2.add_axes([0.2,0.2,0.7,0.7])
ax2.plot(stock_data51['return'].values)

stock_data52 = stock_data[stock_data['code'] == stk_codes[2]]
stock_data52['date'] = pd.to_datetime(stock_data52['date'])
stock_data52.sort_values(by=['date'], inplace=True)
stock_data52['return'] = np.log(stock_data52['close']) - np.log(stock_data52['close'].shift(periods=1))
stock_data52.dropna(inplace=True)
ind = (stock_data52['return'] >= -0.1) & (stock_data52['return'] <= 0.1)
stock_data52 = stock_data52.loc[ind, :]

fig3=plt.figure()
ax3=fig3.add_axes([0.2,0.2,0.7,0.7])
ax3.plot(stock_data52['return'].values)

stock_data53 = stock_data[stock_data['code'] == stk_codes[3]]
stock_data53['date'] = pd.to_datetime(stock_data53['date'])
stock_data53.sort_values(by=['date'], inplace=True)
stock_data53['return'] = np.log(stock_data53['close']) - np.log(stock_data53['close'].shift(periods=1))
stock_data53.dropna(inplace=True)
ind = (stock_data53['return'] >= -0.1) & (stock_data53['return'] <= 0.1)
stock_data53 = stock_data53.loc[ind, :]

stock_data54 = stock_data[stock_data['code'] == stk_codes[4]]
stock_data54['date'] = pd.to_datetime(stock_data54['date'])
stock_data54.sort_values(by=['date'], inplace=True)
stock_data54['return'] = np.log(stock_data54['close']) - np.log(stock_data54['close'].shift(periods=1))
stock_data54.dropna(inplace=True)
ind = (stock_data54['return'] >= -0.1) & (stock_data54['return'] <= 0.1)
stock_data54 = stock_data54.loc[ind, :]


stock1 = pd.read_csv('../data/1EShowData_data_stock_daily_price_2001-2018.csv',
                     encoding='GB2312',
                     usecols=[1, 5, 10])   #导入指数数据
stock1.columns = ['date', 'close', 'rfreturn']
stock1.dropna(inplace=True)
stock1['date'] = pd.to_datetime(stock1['date'])
stock1['return'] = np.log(stock1['close']) - np.log(stock1['close'].shift(periods=1))
stock1.dropna(inplace=True)
ind = (stock1['return'] >= -0.1) & (stock1['return'] <= 0.1)
stock1 = stock1.loc[ind, :]


index = pd.read_csv('../data/1EShowData_data_Index_daily_price_2001-2018.csv',
                    encoding='GB2312',
                    usecols=[1, 5])
index.columns = ['date', 'close']
index['date'] = pd.to_datetime(index['date'])
index['return'] = np.log(index['close']) - np.log(index['close'].shift(periods=1))
index.dropna(inplace=True)
ind = (index['return'] >= -0.1) & (index['return'] <= 0.1)
index = index.loc[ind, :]

#数据洗好之后横着拼起来,以date为共同参考系,suffixes替换两个相同return的列名
data_matrix = pd.merge(left=index[['date', 'return']],
                      right=stock1[['date', 'return']],
                      on='date',
                      how='inner',
                      sort=True,
                      suffixes=('', '1'))

data_matrix = pd.merge(left=data_matrix,
                      right=stock_data50[['date', 'return']],
                      on='date',
                      how='inner',
                      sort=True,
                      suffixes=('', '2'))

data_matrix = pd.merge(left=data_matrix,
                      right=stock_data51[['date', 'return']],
                      on='date',
                      how='inner',
                      sort=True,
                      suffixes=('', '3'))
data_matrix = pd.merge(left=data_matrix,
                      right=stock_data52[['date', 'return']],
                      on='date',
                      how='inner',
                      sort=True,
                      suffixes=('', '4'))
data_matrix = pd.merge(left=data_matrix,
                      right=stock_data53[['date', 'return']],
                      on='date',
                      how='inner',
                      sort=True,
                      suffixes=('', '5'))
data_matrix = pd.merge(left=data_matrix,
                      right=stock_data54[['date', 'return']],
                      on='date',
                      how='inner',
                      sort=True,
                      suffixes=('', '6'))

#导入无风险利率
ret_rf = stock_data[['date', 'rfreturn']]
ret_rf.drop_duplicates(inplace=True, subset=['date'])
ret_rf['date'] = pd.to_datetime(ret_rf['date'])
ret_rf.sort_values(by=['date'], inplace=True)
data_matrix = pd.merge(left=data_matrix,
                      right=ret_rf[['date', 'rfreturn']],
                      on='date',
                      how='inner',
                      sort=True)

data_matrix.columns = ['date', 'ind', 'stk1', 'stk2', 'stk3', 'stk4', 'stk5', 'stk6', 'rf']
print(data_matrix)

data_matrix['ind'] = data_matrix['ind'] - data_matrix['rf']
data_matrix['stk1'] = data_matrix['stk1'] - data_matrix['rf']
data_matrix['stk2'] = data_matrix['stk2'] - data_matrix['rf']
data_matrix['stk3'] = data_matrix['stk3'] - data_matrix['rf']
data_matrix['stk4'] = data_matrix['stk4'] - data_matrix['rf']
data_matrix['stk5'] = data_matrix['stk5'] - data_matrix['rf']
data_matrix['stk6'] = data_matrix['stk6'] - data_matrix['rf']
# index=['ind', 'stk1', 'stk2', 'stk3', 'stk4', 'stk5', 'stk6', 'rf']
# cols = ['ind', 'stk1', 'stk2', 'stk3', 'stk4', 'stk5', 'stk6']
# data_matrix[cols] = data_matrix[cols].sub(data_matrix['rf'], axis=0)
#可改成这样更简洁

#进行CAPM检验
ret_ind = data_matrix['ind'].values   #把这个当自变量
T = len(ret_ind)
N = 6  #体现矩阵维度,方便后面回归
mu_market = np.mean(ret_ind)
sigma_market = np.sum((ret_ind-mu_market)**2)/T

ret_stocks = data_matrix[['stk1', 'stk2', 'stk3', 'stk4', 'stk5', 'stk6']].values

x = np.ones((T, 2))
x[:, 1] = ret_ind   #第0列是全一列,第一列才是指数

y = ret_stocks
xTx = np.dot(np.transpose(x), x)
xTy = np.dot(np.transpose(x), y)
AB_hat = np.dot(np.linalg.inv(xTx), xTy)
ALPHA = AB_hat[0]
print("CAPM回归的阿尔法为:",ALPHA)
BETA = AB_hat[1]
RESD = y - np.dot(x, AB_hat)
COV = np.dot(np.transpose(RESD), RESD)/T
invCOV = np.linalg.inv(COV)



#这是强制过原点回归
xr = np.ones((T, 1))
xr[:, 0] = ret_ind
yr = ret_stocks
xrTxr = np.dot(np.transpose(xr), xr)
xrTyr = np.dot(np.transpose(xr), yr)
ABr_hat = np.dot(np.linalg.inv(xrTxr), xrTyr)
RESDr = yr - np.dot(xr, ABr_hat)
COVr = np.dot(np.transpose(RESDr), RESDr)/T
invCOVr = np.linalg.inv(COVr)


#后续为更高深的检验,看不懂,考了算他牛逼
trans_ALPHA = np.ones((len(ALPHA), 1))
trans_ALPHA[:, 0] = ALPHA
SWchi2 = T*(1/(1+mu_market**2/sigma_market))*np.dot(np.dot(ALPHA, invCOV), trans_ALPHA)
SWF = (T-N-1)/N*(1/(1+mu_market**2/sigma_market))*np.dot(np.dot(ALPHA, invCOV), trans_ALPHA)
pvalue_Wchi2 = 1 - chi2.cdf(SWchi2[0], N)
pvalue_WF = 1 - f.cdf(SWF[0], N, T-N-1)
print(pvalue_Wchi2)
print(pvalue_WF)
SLRchi2 = T*(np.log(np.linalg.det(COVr)) - np.log(np.linalg.det(COV)))
pvalue_SLRchi2 = 1 - chi2.cdf(SLRchi2, N)
print(pvalue_SLRchi2)
a = np.zeros((6, 1))
a[:, 0] =  np.sum(RESDr, axis=0)
salpha = np.dot(invCOVr, a)
b = np.dot(ret_ind, RESDr)
sbeta = np.zeros((6,1))
sbeta[:, 0] = np.dot(invCOVr, b)
score = np.concatenate((salpha, sbeta), axis=0)
print(score)
a = np.concatenate((invCOVr*T, invCOVr*np.sum(ret_ind)), axis=1)
b = np.concatenate((invCOVr*np.sum(ret_ind), invCOVr*np.sum(ret_ind**2)), axis=1)
Minfo = np.concatenate((a, b), axis=0)
SLMchi2 = np.dot(np.dot(np.transpose(score), np.linalg.inv(Minfo)), score)
pvalue_SLMchi2 = 1-chi2.cdf(SLMchi2[0][0], N)
print(pvalue_SLMchi2)