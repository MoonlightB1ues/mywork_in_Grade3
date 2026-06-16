import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import chi2, f
import warnings
warnings.filterwarnings("ignore")
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
index=pd.read_csv('../data/RESSET_IDXMONRET_1.csv')
index.columns = ["cd",'date', 'return']
index['date'] = pd.to_datetime(index['date']).dt.to_period('M')
index.dropna(inplace=True)
print(index)
ind = (index['return'] >= -0.1) & (index['return'] <= 0.1)
index = index.loc[ind, :]

#多资产联合检验

stock_data=pd.read_csv('../data/RESSET_MRESSTK_1 (1).csv')
stock_data.sort_values("Stkcd",inplace=True)
# print(stock_data)
# print(np.sum(stock_data.isnull(),axis=0))
stock_data.dropna(inplace=True)

stock_data.columns=["code","date","close","rf"]
stk_codes = np.unique(stock_data['code'].values)
# print(stk_codes)
#清洗数据,思路为先把数据拆开,得到收益率
for i in np.arange(len(stk_codes)):
    df=stock_data[stock_data['code'] == stk_codes[i]]
    df["date"] = pd.to_datetime(df['date']).dt.to_period('M')
    df.sort_values("date",inplace=True)
    df[f"return{i}"]=np.log(df['close']) - np.log(df['close'].shift(periods=1))
    df.dropna(inplace=True)
    ind=(df[f"return{i}"]>=-0.1) & (df[f"return{i}"]<=0.1)
    df=df.loc[ind,:]
    globals()[f"stock{i}"]=df #这里虽然跑,但有warning,建议先创建一个列表,把df传进去,索引就是对应股票
    print(df.shape)
# print(stock0)
merge_data=pd.merge(left=stock0[["date","rf","return0"]],right=stock1[["date","return1"]],on="date",how="inner")
print(merge_data.shape)
for i in np.arange(2,3):
    df=globals()[f"stock{i}"]
    merge_data=pd.merge(left=merge_data,right=df[["date",f"return{i}"]],on="date",how="inner")
    print(merge_data.shape)
merge_data=pd.merge(left=merge_data,right=index[["date","return"]],on="date",how="inner")
print(merge_data)
#把三个股票和无风险利率,指数收益拼贴在一起


data_matrix=merge_data
data_matrix.columns = ['date', 'rf', 'stk1', 'stk2',"stk3","ind"]
print(data_matrix)

data_matrix['ind'] = data_matrix['ind'] - data_matrix['rf']
data_matrix['stk1'] = data_matrix['stk1'] - data_matrix['rf']
data_matrix['stk2'] = data_matrix['stk2'] - data_matrix['rf']
data_matrix['stk3'] = data_matrix['stk3'] - data_matrix['rf']

ret_ind = data_matrix['ind'].values   #把这个当自变量
T = len(ret_ind)
N = 6
mu_market = np.mean(ret_ind)
sigma_market = np.sum((ret_ind-mu_market)**2)/T
ret_stocks = data_matrix[['stk1', 'stk2', 'stk3']].values

#多股票检验,这里的阿尔法和贝塔是一个向量
x = np.ones((T, 2))
x[:, 1] = ret_ind
y = ret_stocks
xTx = np.dot(np.transpose(x), x)
xTy = np.dot(np.transpose(x), y)
AB_hat = np.dot(np.linalg.inv(xTx), xTy)
ALPHA = AB_hat[0]
print(ALPHA)
BETA = AB_hat[1]
RESD = y - np.dot(x, AB_hat)
COV = np.dot(np.transpose(RESD), RESD)/T
invCOV = np.linalg.inv(COV)

xr = np.ones((T, 1))
xr[:, 0] = ret_ind
yr = ret_stocks
xrTxr = np.dot(np.transpose(xr), xr)
xrTyr = np.dot(np.transpose(xr), yr)
ABr_hat = np.dot(np.linalg.inv(xrTxr), xrTyr)
RESDr = yr - np.dot(xr, ABr_hat)
COVr = np.dot(np.transpose(RESDr), RESDr)/T
invCOVr = np.linalg.inv(COVr)



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
a = np.zeros((3, 1))
a[:, 0] =  np.sum(RESDr, axis=0)
salpha = np.dot(invCOVr, a)
b = np.dot(ret_ind, RESDr)
sbeta = np.zeros((3,1))
sbeta[:, 0] = np.dot(invCOVr, b)
score = np.concatenate((salpha, sbeta), axis=0)
print(score)
a = np.concatenate((invCOVr*T, invCOVr*np.sum(ret_ind)), axis=1)
b = np.concatenate((invCOVr*np.sum(ret_ind), invCOVr*np.sum(ret_ind**2)), axis=1)
Minfo = np.concatenate((a, b), axis=0)
SLMchi2 = np.dot(np.dot(np.transpose(score), np.linalg.inv(Minfo)), score)
pvalue_SLMchi2 = 1-chi2.cdf(SLMchi2[0][0], N)
print(pvalue_SLMchi2)