from datetime import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.io import loadmat
from envs.my_pythorch.Lib.pydoc import describe
from pandas.core.interchange.dataframe_protocol import DataFrame
from sqlalchemy import column

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
# mat_data = loadmat("4实验数据-SSEC_min.mat")
#
# for key in mat_data.keys():
#     if not key.startswith("__"):  # 过滤掉内部属性
#         print(key)
#
# df = pd.DataFrame({k: mat_data[k].squeeze() for k in ["d","p","t"]})
# print(df.head(),df.shape)
# df.to_pickle("data.pkl")


data = pd.read_pickle("../data/data.pkl")
print(data)
data['d'] = data['d'].apply(lambda x: str(x[0]))  #因为原数据对应的列是列表形式,需要把列表里的值取出来
data['t'] = data['t'].apply(lambda x: str(x[0]))
print(data)
data["t1"]=data["t"]
data['t'] = data['d'].astype(str) + ' ' + data['t'].astype(str)

data["t"]=pd.to_datetime(data["t"],format='mixed')
# data['dt']=data['t'].diff()  #取时间间隔
# data['dt'] = data['dt'].dt.total_seconds() / 60  #单位取至分钟

data.set_index('t', inplace=True)
data = data.groupby(level=0).last()
# 定义你需要的时间间隔字典
# pandas的频率别名：'min' 或 'T' 代表分钟
intervals = {
    '1': '1min',
    '5': '5min',
    '10': '10min',
    '30': '30min',
    '60': '60min',
}
return_dl = {} #这是一个字典

# 1. 检查索引是否唯一（如果输出 False，说明此时已经重复了）
print("索引是否唯一:", data.index.is_unique)

# 2. 打印出前 10 条完全重复的时间戳和对应的数据
print("重复的数据样本:")
print(data[data.index.duplicated(keep=False)].head(10))

for name, freq in intervals.items():
    # 先 ffill 填补盘中可能因为停牌缺失的分钟，再取 las
    resampled_p = data['p'].resample(freq).last().ffill()
        # 2. 剔除非交易时间
    # 提取时间部分用于比对
    times = resampled_p.index.time
    # 设定A股的有效交易时间掩码 (根据你的市场可自行修改)
    valid_time_mask = ((times >= time(9, 30)) & (times <= time(11, 30))) | \
                      ((times >= time(13, 0)) & (times <= time(15, 0)))
    # 过滤出真正交易的时间段
    valid_p = resampled_p[valid_time_mask].copy()
    # 3. 创建“交易节” (Session) 标签
    # 提取日期
    dates = valid_p.index.date
    # 判断是上午盘(AM)还是下午盘(PM)
    ampm = np.where(valid_p.index.time < time(12, 0), 'AM', 'PM')
    # 把日期和上下午拼接，作为分组的唯一标识符，例如 "2023-10-10_AM"
    session_groups = [f"{d}_{s}" for d, s in zip(dates, ampm)]
    # 4. 在同一个 Session 内计算收益率
    # groupby 会确保 13:00 的数据不会去跟 11:30 的数据计算收益率，而是返回 NaN
    ret = valid_p.groupby(session_groups).pct_change().round(3)
    return_dl[f'{name}'] = ret

data['t1']=pd.to_datetime(data['t1'],format='%H:%M')
data['dt']=data['t1'].diff()
data['dt'] = data['dt'].dt.total_seconds() / 60
data = data[data['dt'] == 1]
return_dl["120"]= (data['p'] / data['p'].shift(120)).round(3)-1
return_dl["240"]= (data['p'] / data['p'].shift(240)).round(3)-1

returns=return_dl["1"]
returns = returns.replace([np.inf, -np.inf], np.nan).dropna()
values, counts = np.unique(returns, return_counts=True)
frequency = counts /sum(counts)
print(frequency,values)

fig=plt.figure()
ax=fig.add_axes([0.2,0.2,0.7,0.7])
plt.xlim(-0.02, 0.02)
plt.ylim(1e-5, 1)
ax.set_yscale('log')
for i in [1,5,10,30,60,120,240]:
    returns = return_dl[f'{i}']
    returns = returns.replace([np.inf, -np.inf], np.nan).dropna()  #将极限值np.inf替代为nan然后去掉
    values, counts = np.unique(returns, return_counts=True)
    if i == 1:  # 保存 t=1 的统计特征用来对比
        base_mu, base_std = returns.mean(), returns.std()
    frequency = counts / sum(counts)
    ax.plot(values, frequency, 'o-', ms=4,mfc='none',label=f"t={i}minute")


x=np.arange(-0.005,0.005)
y = norm.pdf(x, loc=base_mu, scale=base_std)
ax.plot(x,y, 'o-', ms=4,mfc='none',label="normal distribution")  #因为数量级的原因,所以图像里显示不出来

ax.legend(loc="upper right",fontsize=6 )
plt.show()


