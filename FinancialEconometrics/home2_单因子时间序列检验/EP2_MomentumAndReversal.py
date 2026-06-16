import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import chi2, f
import warnings
import glob
warnings.filterwarnings("ignore")

file_list = glob.glob("../data/home2/*.csv")
database=[pd.read_csv(f) for f in file_list]
data = pd.concat(database,axis=0,ignore_index=True)
data.columns=["code","date","close"]
data.dropna(inplace=True)
data["date"] = pd.to_datetime(data["date"],format="%Y-%m-%d").dt.to_period("M")
# print(data.head())

data["code"]=pd.to_numeric(data["code"])
data.sort_values("code",inplace=True)
data.dropna(inplace=True)

stk_codes=np.unique(data["code"].values)
# print(stk_codes)


stk_base=[]
for i in np.arange(len(stk_codes)):
    df=data[data['code'] == stk_codes[i]]
    df.sort_values("date",inplace=True)
    df["return"]=np.log(df['close']) - np.log(df['close'].shift(periods=1))
    df.dropna(inplace=True)
    globals()[f"stock{i}"]=df
    stk_base.append(df)


stk_data=pd.concat(stk_base,axis=0,ignore_index=True)

stk_data.drop_duplicates(inplace=True, subset=['date',"code"])

all_months = sorted(stk_data['date'].unique())
print(len(all_months))
results = []

for N in [1]:
    M=N
    all_series = [[] for _ in range(5)]
    for i in range(len(all_months) - M):
        curr_turn = all_months[i]
        next_turn = all_months[i + M]
        data_curr = stk_data[stk_data["date"] == curr_turn].copy()
        data_next = stk_data[stk_data["date"] == next_turn].copy()
        data_curr.sort_values("return", inplace=True)
        group_codes = data_curr["code"].unique()
        chunks = np.array_split(group_codes, 5)
        for idx, chunk in enumerate(chunks):
            # A. 计算当月该组的平均收益
            group_curr_data = data_curr[data_curr['code'].isin(chunk)]
            avg_ret_curr = group_curr_data['return'].mean()
            # B. 计算下个月该组的平均收益
            # 注意：这里是用当月分好的股票去匹配下个月的收益
            group_next_data = data_next[data_next['code'].isin(chunk)]
            avg_ret_next = group_next_data['return'].mean()
            effect = avg_ret_next - avg_ret_curr
            all_series[idx].append(effect)
        df_input = {f"effect{i+1}": pd.Series(all_series[i]) for i in range(5)}
    stkN1 = pd.DataFrame(df_input)
    print(stkN1)
results_all = {}
for N in [3,6,12]:
    M=N
    all_series = [[] for _ in range(5)]
    storage = [[] for _ in range(5)]
    for i in range(N, len(all_months) - M):

        lookback_months = all_months[i - N: i]  # 前N个月
        formation_month = all_months[i - 1]
        holding_months = all_months[i: i + M]  # 后 M 个月
        data_lookback = stk_data[stk_data['date'].isin(lookback_months)]
        momentum_signal = data_lookback.groupby('code')['return'].sum().reset_index()   # 返回的仍然是一个数据框,只是其中每个股票的收益率被求和了
        momentum_signal.rename(columns={'return': 'cum_return'}, inplace=True)
        # 3. 分组 (根据回溯期的累计收益率)
        momentum_signal.sort_values("cum_return", inplace=True)
        # 剔除空值
        momentum_signal = momentum_signal.dropna(subset=['cum_return'])
        group_codes = momentum_signal["code"].unique()
        chunks = np.array_split(group_codes, 5)

        # 4. 计算持有期 M 个月的收益
        data_holding = stk_data[stk_data['date'].isin(holding_months)]

        for idx, chunk in enumerate(chunks):
            # 筛选出这组股票在持有期的数据
            group_holding_data = data_holding[data_holding['code'].isin(chunk)]
            # 计算该组在 M 个月内的平均表现
            # 这里通常先算每只股票在 M 个月内的累计收益，再取组平均
            indiv_cum_ret = group_holding_data.groupby('code')['return'].sum()
            avg_effect = indiv_cum_ret.mean()
            storage[idx].append(avg_effect)
    df_name = f"Mom_{N}_{M}"
    results_all[df_name] = pd.DataFrame({ f"Group_{k + 1}": pd.Series(storage[k]) for k in range(5)})
results_all["Mom_1_1"]=stkN1
print(results_all["Mom_3_3"].head())

fig=plt.figure()
ax=fig.add_subplot(2,2,1)
ax.plot(results_all["Mom_1_1"])
ax.legend(["low return","return1","return2","return3","high return"],fontsize=6)
ax.set_title("N,M=1",fontsize=8)

ax_1=fig.add_subplot(2,2,2)
ax_1.set_title("N,M=3",fontsize=8)
ax_1.plot(results_all["Mom_3_3"])
ax_1.legend(["low return","return1","return2","return3","high return"],fontsize=6)

ax_2=fig.add_subplot(2,2,3)
ax_2.set_title("N,M=6",fontsize=8)
ax_2.plot(results_all["Mom_3_3"])
ax_2.legend(["low return","return1","return2","return3","high return"],fontsize=6)

ax_3=fig.add_subplot(2,2,4)
ax_3.set_title("N,M=12",fontsize=8)
ax_3.plot(results_all["Mom_12_12"])
ax_3.legend(["low return","return1","return2","return3","high return"],fontsize=6)

plt.show()