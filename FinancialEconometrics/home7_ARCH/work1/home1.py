import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import warnings
from scipy.stats import kurtosis
from sklearn.metrics import r2_score
from statsmodels.stats.diagnostic import het_arch
from arch import arch_model   #引用类方法
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
from statsmodels.tsa.ar_model import AutoReg

#感觉还是这样读文件比较通用
file_list = glob.glob("data/RESSET_DR*.xlsx")
data = pd.concat((pd.read_excel(f) for f in file_list), axis=0, ignore_index=True)
data.columns=["cd","name","state","date","close"]
data_name=data["name"].unique()
data["date"]=pd.to_datetime(data["date"],format='%Y-%m-%d')
data.dropna(inplace=True)
data.duplicated(subset=['date'],keep="first")
#多文件导入


index_list=glob.glob("data/RESSET_ID*.csv")
index =pd.concat((pd.read_csv(f,encoding='GB2312') for f in index_list), axis=0, ignore_index=True)   #or ETF-8
index.dropna(inplace=True)
index.columns=["cd","date","close","r"]
index.duplicated(subset=['date'],keep="first")
print(index["cd"].unique())



index_01 = index[index["cd"]==1]
index_02 = index[index["cd"]==399001]


data_sihuan=data[data["name"]==data_name[0]].copy()
data_changhong=data[data["name"]==data_name[1]].copy()
# print(data_sihuan)
# print(data_changhong.shape)

data_sihuan.sort_values('date', ascending=True,inplace=True)
data_changhong.sort_values('date', ascending=True,inplace=True)

data_sihuan["r"]=data_sihuan["close"]-data_sihuan["close"].shift(1)
data_changhong["r"]=data_changhong["close"]-data_changhong["close"].shift(1)
data_sihuan.dropna(inplace=True)
data_changhong.dropna(inplace=True)


fig=plt.figure()
axes = [] # 创建一个空列表来存放子图
i=0
for j in range(1, 13): # 4行3列，共12个图
    # 将生成的子图追加到列表中
    ax = fig.add_subplot(3, 4, j)  #把建立的子图存在axes中
    axes.append(ax)


def des_r(stock):  #传的是一个dataframe,r为收益率向量
    r = stock['r'].to_numpy()
    trday = len(r)
    mean_r = np.mean(r)
    std_r = np.std(r)
    max_r = np.max(r)
    min_r = np.min(r)
    k_value = kurtosis(r, fisher=True, bias=False)
    selfre_1 = np.corrcoef(r[0:-1], r[1:])[0, 1]
    return trday, mean_r, std_r, max_r, min_r, k_value,selfre_1

def testify(stock,m):   #m为lag阶数
    r = stock['r']
    r_bar=r.mean()
    r_dec=r-r_bar
    lm_stat, p_value, f_stat, fp_value = het_arch(r_dec, nlags=m)
    return lm_stat, p_value, f_stat, fp_value


lm_stat, p_value, f_stat, fp_value=testify(data_changhong,5)
print(f"--- Engle's ARCH 检验结果 (滞后 {5} 阶) ---")
print(f"LM 统计量 (LM Statistic): {lm_stat:.4f}")
print(f"LM p-值 (p-value): {p_value:.4e}")
print(f"F 统计量 (F Statistic): {f_stat:.4f}")
print(f"F p-值 (F p-value): {fp_value:.4e}")



def arch_test(stock):
    global i
    r = stock['r'].to_numpy()
    am_arch = arch_model(r * 100, mean='constant', vol='ARCH', p=1, q=1, dist='normal')  # 定义类
    res = am_arch.fit()
    sim = arch_model(None, mean='constant', vol='ARCH', p=1, q=1, dist='normal')
    sim_data = sim.simulate(res.params, len(r))
    axes[i].plot(sim_data["data"]/100,label='sim')
    axes[i].plot(r,label="real")
    axes[i].legend(loc='best',fontsize=6)
    i=i+1
    return res

sihuan_test1 = arch_test(data_sihuan)
changhong_test1 = arch_test(data_changhong)
index_01_test1 = arch_test(index_01)
index_02_test2 = arch_test(index_02)

def garch_test(stock):
    global i
    r = stock['r'].to_numpy()
    am = arch_model(r * 100, mean='constant', vol='GARCH', p=1, q=1, dist='normal')  # 定义类
    res = am.fit()
    sim_garch = arch_model(None, mean='constant', vol='garch', p=1, q=1, dist='normal')
    sim_data = sim_garch.simulate(res.params, len(r))
    axes[i].plot(sim_data["data"]/100,label='sim')
    axes[i].plot(r,label="real")
    axes[i].legend(loc='best',fontsize=6)
    i=i+1
    return res

sihuan_test2 = garch_test(data_sihuan)
changhong_test2 = garch_test(data_changhong)
index_01_test2 = garch_test(index_01)
index_02_test2 = garch_test(index_02)

def egarch_test(stock):
    global i
    r = stock['r'].to_numpy()
    am = arch_model(r * 100, mean='constant', vol='EGARCH', p=1, q=1, o=1, dist='normal')  #记得加o=1
    res = am.fit()
    sim_garch = arch_model(None, mean='constant', vol='EGARCH', p=1,o=1, q=1, dist='normal')
    sim_data = sim_garch.simulate(res.params, len(r))
    axes[i].plot(sim_data["data"]/100,label='sim')
    axes[i].plot(r,label="real")
    axes[i].legend(loc='best',fontsize=6)
    i=i+1
    return res

sihuan_test3 = egarch_test(data_sihuan)
changhong_test3 = egarch_test(data_changhong)
index_01_test3 = egarch_test(index_01)
index_02_test3 = egarch_test(index_02)
print(sihuan_test3)

plt.subplots_adjust(wspace=0.3, hspace=0.4)
for ax in axes:
    # --- 这里放你的实际画图代码 ---
    # 3. 将坐标轴的刻度字体缩小 (labelsize=8 或者更小)
    ax.tick_params(axis='both', which='major', labelsize=8)
plt.show()

