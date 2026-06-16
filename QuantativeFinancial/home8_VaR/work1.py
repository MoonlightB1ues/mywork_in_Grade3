import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
from bs4 import BeautifulSoup
import time
import random
import glob
import re
import statsmodels.api as sm
from scipy.stats import chi2,f,genpareto
from scipy.stats import norm
from scipy.io import loadmat
import statsmodels.formula.api as smf
from sklearn import linear_model
from scipy import stats
from datetime import datetime, timedelta
from scipy.stats import kurtosis
from arch import arch_model
from statsmodels.tsa.ar_model import AutoReg


import warnings
warnings.filterwarnings('ignore')

# 设置显示最多 20 列
pd.set_option('display.max_columns', 20)
# 设置显示最多 50 行
pd.set_option('display.max_rows', 50)
# 设置显示宽度，确保 20 列尽量在一行内显示，不换行
pd.set_option('display.width', 1000)
np.set_printoptions(
    linewidth=1000,    # 每行最多显示多少个字符，防止折行
    threshold=1000,    # 数组元素总数超过这个值时，中间部分会显示为省略号 ...
    precision=4,       # 小数点后保留几位
    suppress=True      # 禁用科学计数法，强制显示小数
)



class Task2_SinaDataFetcher:
    """任务二：新浪财经历史行情数据获取"""
    def __init__(self,stock_code,datalen=1000):
        self.stock_code = stock_code
        self.datalen = datalen
        self.url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh{stock_code}&scale=240&ma=no&datalen={datalen}"
        self.output_file = "mydata_000006.txt"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
    def run(self):
        print(f"--- 开始执行任务 2：拉取新浪财经 K线数据 ---")
        try:
            resp = requests.get(self.url, headers=self.headers, timeout=10)
            data = json.loads(resp.text)
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write("Date,Open,High,Low,Close,Volume\n")
                for day_data in data:
                    line = f"{day_data['day']},{day_data['open']},{day_data['high']},{day_data['low']},{day_data['close']},{day_data['volume']}"
                    f.write(line + "\n")
            print(f"任务 2 完成，共获取 {len(data)} 个交易日数据，已保存至 {self.output_file}\n")
        except Exception as e:
            print(f"任务 2 执行失败: {e}")
# fetcher = Task2_SinaDataFetcher(stock_code="000006",datalen=10000)
# fetcher.run()


data=pd.read_csv("mydata_000006.txt")

def data_clean(data,h=0):  #如果要算更复杂的参数,令h=1
    data.columns=['date','open','high','low','close','volume']  #该行需要自行判断,将所有的列改成你熟悉的形式
    data["date"]=pd.to_datetime(data["date"],format='%Y-%m-%d') #时间的格式也需要自己判断
    data.dropna(inplace=True)
    data.duplicated(subset=['date'],keep='first')

    data["yearmonth"]=data['date'].dt.strftime('%Y%m').astype(int)
    data["r"] = data["close"].apply(np.log) - data["close"].shift(1).apply(np.log)
    data.dropna(inplace=True)
    if h==1:
        #如果是月度数据,算月波动率
        vol = data.groupby("yearmonth")["r"].agg(lambda x: (x ** 2).sum()).reset_index()
        vol.rename(columns={"r": "vol"}, inplace=True)
        # 算股价高点
        hpoint = data.groupby("yearmonth")["close"].max().reset_index()
        hpoint.rename(columns={"close": "hpoint"}, inplace=True)
        # 月已实现偏度
        skewness = data.groupby("yearmonth")["close"].agg(
            lambda x: ((x ** 3).sum()) * len(x) ** 0.5 / ((x ** 2).sum()) ** 1.5).reset_index()
        skewness.rename(columns={"close": "skewness"}, inplace=True)
        data = pd.merge(left=data, right=vol[["vol", "yearmonth"]], on="yearmonth", how="left")
        data = pd.merge(left=data, right=hpoint[["hpoint", "yearmonth"]], on="yearmonth", how="left")
        data = pd.merge(left=data, right=skewness[["skewness", "yearmonth"]], on="yearmonth", how="left")
        data["exr"] = data["r"] - data["rf"]  #需要原数据有无风险利率
    return data

data=data_clean(data)
print(data)
r=data["r"]
r_samplein=data[data.index<len(data)/2]["r"]
r_sampleout=data[data.index>=len(data)/2]["r"]

def RiskMetrics(r,t,alpha=0.05):  #t为回撤天数,即算分布的时候包含多少样本量,假设分布为正态分布,-VaR=mu_t+Z_alpha*sigma
    l = np.fix(len(data)/5).astype(int)   #l指定从什么时候开始测
    VaR_RM = np.zeros(len(r))
    qalpha = norm.ppf(alpha)
    for i in range(l, len(r)):
        mhat, shat = norm.fit(r[i-t:i])      #根据历史数据估计出均值与方差
        VaR_RM[i] = (mhat + qalpha*shat)*-1
    return VaR_RM

def experience(r,t,alpha=0.05):
    l = np.fix(len(data)/5).astype(int)
    VaR_RM = np.zeros(len(r))
    for i in range(l, len(r)):
        VaR_RM[i] = np.percentile(r[i-t:i], alpha * 100)
    return -VaR_RM

def GARCH_Normal(r,t,alpha=0.05):   #文档里说的是Gamma方法,应该是弄错了,这显然用的是GARCH模型.要估计第n期的波动率,是拿n-t到n-1期的原始数据进行估计
    VaR_GN = np.zeros(len(r))        #注意,这里的r应该是numpy形式,否则dataframe自带的索引会使数据对齐出现错误
    l = np.fix(len(data) / 5).astype(int)
    qalpha = norm.ppf(alpha)  #算出Z_alpha
    for i in range(l, len(r)):
        am_ar_garch = arch_model(r[i-t:i], mean='AR', lags=1, vol='GARCH', p=2, q=2, dist='normal')  #r[],左开右闭哈
        res_ar_garch = am_ar_garch.fit(disp='off') #传递拟合参数
        a = res_ar_garch.forecast(horizon=1, align='origin')  #使用拟合参数进行预测
        mu = a.mean['h.1'].iloc[-1]         #预测第n期的均值与方差
        sgm2 = a.variance['h.1'].iloc[-1]
        VaR_GN[i] = -(mu + qalpha*np.sqrt(sgm2))
    return VaR_GN

def POT(r,p,alpha=0.05):  #p为阈值所在点占总体的分位数
    # POT方法
    VaR_EVT = np.zeros(len(r))   #生成初始向量
    l = np.fix(len(data) / 5).astype(int)

    for i in range(l, len(r)):
        his_sample = r[i-200:i]
        his_sample = np.sort(his_sample)   #默认从低到高排列,his_sample = np.sort(his_sample)[::-1]为降序排列
        ind = np.fix(len(his_sample)*p).astype(int)  #找出分位数临界点,fix是向下取,然后取整
        evt_sample = np.abs(his_sample[:ind])   #找出大于分位点的值,并取绝对值
        #然后构建统计量,不用理解,复制粘贴即可
        u = np.abs(his_sample[ind])
        exceed_values = evt_sample - u
        n = len(his_sample)
        Nu = len(exceed_values)
        parmhat = genpareto.fit(exceed_values, floc=0)
        print(parmhat)
        kHat = parmhat[0] # tail index
        sigmaHat = parmhat[2] # scale parameter
        VaR_EVT[i] = u + sigmaHat / kHat * ((alpha*n/Nu)**-kHat -1)
    return VaR_EVT

#四个方法都是算VaR值的,返回的都是正的VaR


VaR_RN =GARCH_Normal(r,100,alpha=0.05)
VaR_RM=RiskMetrics(r,100,alpha=0.05)
exp_RM=experience(r,200,alpha=0.05)
VaR_POT=POT(r,0.1,alpha=0.05)
fig=plt.figure()
ax1=fig.add_axes((0.1,0.1,0.8,0.8))
# ax1.plot(r)
ax1.plot(-VaR_RM,label='Risk Metric')
ax1.plot(-exp_RM,label='Experience')
ax1.plot(-VaR_RN,label='GARCH')
ax1.plot(-VaR_POT,label="Pareto")
plt.legend()
plt.show()

VaR_HS=exp_RM
VaR_EVT=VaR_POT
VaR_GN=VaR_RN


data = pd.DataFrame({'return': r,
                     'VaR_RM': VaR_RM,
                     'VaR_GN': VaR_RN,
                     'VaR_HS': exp_RM,
                     'VaR_EVT': VaR_POT})
data.to_csv('Data_VaR.csv')


#检验VaR是否可信,也就是在检验算VaR用到的分布是否合适

def myfun_Kupiec(r, VaR, pstar):   #r为收益率的np格式,Kupiec检验
    N = np.sum(r < -1*VaR)
    T = len(r)
    LRuc = -2*((T-N)*np.log(1-pstar)+N*np.log(pstar)) + 2*((T-N)*np.log(1-N/T)+np.log(N/T)*N)
    pvalue_LRuc = 1 - chi2.cdf(LRuc, 1)
    return LRuc, pvalue_LRuc

def myfun_Christoffersen(r, VaR): #Christoffersen检验
    ind = r < -1*VaR
    ind1 = ind[:-1]   #取不到总值
    ind2 = ind[1:]    #取不到初值,lag1
    n00 = np.sum((ind1==0) & (ind2==0))  #不赖
    n01 = np.sum((ind1==0) & (ind2==1))
    n10 = np.sum((ind1==1) & (ind2==0))
    n11 = np.sum((ind1==1) & (ind2==1))
    Pi01 = n01/(n01+n00)
    Pi11 = n11/(n10+n11)
    Pi2 = (n01+n11)/(n00+n01+n10+n11)
    LRind = (n00+n10)*np.log(1-Pi2) + (n01+n11)*np.log(Pi2) - \
            n00*np.log(1-Pi01) - n01*np.log(Pi01) - n10*np.log(1-Pi11) - n11*np.log(Pi11)
    LRind = LRind*-2
    pvalue_LRind = 1-chi2.cdf(LRind, 1)
    return LRind, pvalue_LRind

def myfun_Kupiec_Christoffersen(LRuc, LRind):  #条件覆盖检验
    LRcc = LRuc + LRind
    pvalue_LRcc = 1-chi2.cdf(LRcc, 2)
    return LRcc, pvalue_LRcc

pstar = 0.05
[LRuc_RM, pvalue_LRuc_RM] = myfun_Kupiec(r, VaR_RM, pstar)
[LRind_RM, pvalue_LRind_RM] = myfun_Christoffersen(r, VaR_RM)
[LRcc_RM, pvalue_LRcc_RM] = myfun_Kupiec_Christoffersen(LRuc_RM, LRind_RM)

[LRuc_GN, pvalue_LRuc_GN] = myfun_Kupiec(r, VaR_GN, pstar)
[LRind_GN, pvalue_LRind_GN] = myfun_Christoffersen(r, VaR_GN)
[LRcc_GN, pvalue_LRcc_GN] = myfun_Kupiec_Christoffersen(LRuc_GN, LRind_GN)

[LRuc_HS, pvalue_LRuc_HS] = myfun_Kupiec(r, VaR_HS, pstar)
[LRind_HS, pvalue_LRind_HS] = myfun_Christoffersen(r, VaR_HS)
[LRcc_HS, pvalue_LRcc_HS] = myfun_Kupiec_Christoffersen(LRuc_HS, LRind_HS)

[LRuc_EVT, pvalue_LRuc_EVT] = myfun_Kupiec(r, VaR_EVT, pstar)
[LRind_EVT, pvalue_LRind_EVT] = myfun_Christoffersen(r, VaR_EVT)
[LRcc_EVT, pvalue_LRcc_EVT] = myfun_Kupiec_Christoffersen(LRuc_EVT, LRind_EVT)

print('{:13s} {:>12s}, {:>12s}, {:>12s}, {:>12s}, {:>12s}, {:>12s}'.format('', 'LRuc', 'pLRuc', 'LRind', 'pLRind', 'LRcc', 'pLRcc'))
print('{:12s}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}'.format('RiskMetrics', LRuc_RM, pvalue_LRuc_RM, LRind_RM, pvalue_LRind_RM, LRcc_RM, pvalue_LRcc_RM))
print('{:12s}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}'.format('GarchNormal', LRuc_GN, pvalue_LRuc_GN, LRind_GN, pvalue_LRind_GN, LRcc_GN, pvalue_LRcc_GN))
print('{:12s}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}'.format('HisSim', LRuc_HS, pvalue_LRuc_HS, LRind_HS, pvalue_LRind_HS, LRcc_HS, pvalue_LRcc_HS))
print('{:12s}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}, {:12.4f}'.format('EVT GPD', LRuc_EVT, pvalue_LRuc_EVT, LRind_EVT, pvalue_LRind_EVT,LRcc_EVT, pvalue_LRcc_EVT))


