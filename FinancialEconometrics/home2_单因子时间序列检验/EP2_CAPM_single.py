import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


plt.rcParams.update({"font.family": "STIXGeneral",
                         "font.size": 20,
                         "mathtext.fontset": "cm"})
data = pd.read_csv("../data/1EShowData_data_stock_daily_price_2001-2018.csv", encoding='GB2312', usecols=[1, 5, 10])
data["r"]=np.log(data["收盘价_Clpr"])-np.log(data["收盘价_Clpr"].shift(1))
data["R"]=data["r"]-data["日无风险收益率_DRfRet"]
data.columns=["date","close","rfreturn","r","R"]

print(np.sum(data.isnull(),axis=0))
data.dropna(inplace=True)
print(data.head())
# print(np.sum(data.isnull(),axis=0))

ind = (data['r'] >= -0.1) & (data['r'] <= 0.1)
data = data.loc[ind, :]

# fig=plt.figure()
# ax=fig.add_axes([0.2,0.2,0.7,0.7])
# ytick=np.arange(-0.1,1.1,0.025)
# plt.yticks(ticks=ytick,fontname='Times New Roman', fontsize=12)
# data['r'].plot()


index_data = pd.read_csv('../data/1EShowData_data_Index_daily_price_2001-2018.csv',
                         encoding='GB2312',
                         usecols=[1, 5])
index_data.columns=['date', 'close']
index_data.dropna(inplace=True)
index_data['return'] = np.log(index_data['close']) - np.log(index_data['close'].shift(periods=1))
index_data.dropna(inplace=True)

fig=plt.figure()
ax=fig.add_axes([0.2,0.2,0.7,0.7])
ytick=np.arange(-0.1,1.1,0.025)
plt.yticks(ticks=ytick,fontname='Times New Roman', fontsize=12)
index_data['return'].plot()


merge_data = pd.merge(left=data[['date', 'r', 'rfreturn']],
                     right=index_data[['date', 'return']],
                        on='date',
                       how='inner')
print(merge_data.head())

##### 以上都是在清洗数据

merge_data.columns = ['date', 'return_stk', 'rfreturn', 'return_ind']
stk_ret = merge_data['return_stk'].values
rf_ret = merge_data['rfreturn'].values
ind_ret = merge_data['return_ind'].values
fig2=plt.figure()
ax2=fig2.add_axes([0.2,0.2,0.7,0.7])
plt.plot(ind_ret - rf_ret, stk_ret - rf_ret, 'o', ms=5, mfc='w', lw=2)
plt.xlabel(r'$r_m - r_f$', fontsize=20)
plt.ylabel(r'$r_i - r_f$', fontsize=20)
plt.savefig(r'C:\Users\Cohen\Desktop\my_plot.png')
plt.show()


X = sm.add_constant(ind_ret-rf_ret)
y = stk_ret - rf_ret
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())
