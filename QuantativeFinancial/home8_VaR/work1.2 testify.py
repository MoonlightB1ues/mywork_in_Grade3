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

data=pd.read_csv("Data_VaR.csv",encoding="utf-8")
data["VaR_EVT"]=-data["VaR_EVT"]
fig=plt.figure()
ax1=fig.add_axes((0.1,0.1,0.8,0.8))
# ax1.plot(r)
ax1.plot(-data["VaR_GN"],label='GARCH')
ax1.plot(-data["VaR_RM"],label='Risk Metric')
ax1.plot(-data["VaR_HS"],label='Experience')
ax1.plot(-data["VaR_EVT"],label="Pareto")
plt.legend()
plt.show()

l = np.fix(len(data) / 5).astype(int)

data1=data[l:].copy()
def myfun_Kupiec(r, VaR, pstar):
    N = np.sum(r < -1*VaR)
    T = len(r)
    LRuc = -2*((T-N)*np.log(1-pstar)+N*np.log(pstar)) + 2*((T-N)*np.log(1-N/T)+np.log(N/T)*N)
    pvalue_LRuc = 1 - chi2.cdf(LRuc, 1)
    return LRuc, pvalue_LRuc


def myfun_Christoffersen(r, VaR):
    # 将布尔值显式转换为 0 和 1 的整数数组，避免类型隐式转换的问题
    ind = (r < -1 * VaR).astype(int)

    ind1 = ind[:-1]  # lag1 (昨日情况)
    ind2 = ind[1:]  # current (今日情况)

    n00 = np.sum((ind1 == 0) & (ind2 == 0))
    n01 = np.sum((ind1 == 0) & (ind2 == 1))
    n10 = np.sum((ind1 == 1) & (ind2 == 0))
    n11 = np.sum((ind1 == 1) & (ind2 == 1))
    print(n00, n01, n10, n11)
    # 安全计算概率，防止分母为 0
    Pi01 = n01 / (n01 + n00) if (n01 + n00) > 0 else 0.0
    Pi11 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0.0
    Pi2 = (n01 + n11) / (n00 + n01 + n10 + n11) if (n00 + n01 + n10 + n11) > 0 else 0.0

    # 闭包函数：安全计算 n * log(p)
    # 基于洛必达法则的极限推导，当 n=0 时，n * log(p) 视作 0
    def safe_log_mult(n, p):
        if n == 0:
            return 0.0
        return n * np.log(p)

    # 计算无约束条件下的对数似然 (Log-likelihood for the alternative)
    ln_L1 = (safe_log_mult(n00, 1 - Pi01) +
             safe_log_mult(n01, Pi01) +
             safe_log_mult(n10, 1 - Pi11) +
             safe_log_mult(n11, Pi11))

    # 计算有约束条件下的对数似然 (Log-likelihood for the null)
    ln_L0 = safe_log_mult(n00 + n10, 1 - Pi2) + safe_log_mult(n01 + n11, Pi2)

    # 计算似然比检验统计量
    LRind = -2 * (ln_L0 - ln_L1)

    # 计算 p-value (自由度为1的卡方分布)
    pvalue_LRind = 1 - chi2.cdf(LRind, 1)

    return LRind, pvalue_LRind

def myfun_Kupiec_Christoffersen(LRuc, LRind):
    LRcc = LRuc + LRind
    pvalue_LRcc = 1-chi2.cdf(LRcc, 2)
    return LRcc, pvalue_LRcc

r=data1["return"].values
VaR_RM=data1["VaR_RM"].values
VaR_GN=data1["VaR_GN"].values
VaR_HS=data1["VaR_HS"].values
VaR_EVT=data1["VaR_EVT"].values
print(data1)
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

