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

data_10=pd.read_csv("../data/RESSET_DRESSTK_2001_2010_1.csv")
data_15=pd.read_csv("../data/RESSET_DRESSTK_2011_2015_1.csv")
data_20=pd.read_csv("../data/RESSET_DRESSTK_2016_2020_1.csv")
data_25=pd.read_csv("../data/RESSET_DRESSTK_2021_2025_1.csv")

stock_data = pd.concat([data_10, data_15,data_20,data_25], ignore_index=True)


stock_data.columns=['cd', 'date', 'close', 'rfreturn']
stock_data['return'] =np.log(stock_data['close']/stock_data['close'].shift(1))
stock_data.dropna(inplace=True)


ind=(stock_data['rfreturn']>-0.1)&(stock_data['rfreturn']<0.1)
stock_data=stock_data.loc[ind,:]

lower_bound = stock_data['return'].quantile(0.01)
upper_bound = stock_data['return'].quantile(0.99)
stock_data['return'] = stock_data['return'].clip(lower=lower_bound, upper=upper_bound)
#强制缩尾处理,把极端值缩减至99%分位数

# print(stock_data)
index=pd.read_csv("../data/RESSET_IDXDRET_1.csv")
index.columns=["date","return_index"]
index.drop_duplicates(inplace=True, subset=['date'])
ind=(index['return_index']>-0.1)&(index['return_index']<0.1)
index=index.loc[ind,:]
print(index)

merge_data=pd.merge(left=stock_data[["date","return","rfreturn"]],right=index[["date","return_index"]],how='inner',on="date",sort=True)
print(merge_data)

ry=merge_data["return"].values
rx=merge_data["return_index"].values
rf=merge_data["rfreturn"].values

ry=ry-rf
rx=rx-rf

draft=pd.DataFrame({"x":rx,"y":ry})
draft = draft.sort_values(by="x")
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(rx,ry,'o', ms=5, mfc='w', lw=2)

X = sm.add_constant(rx)
y = ry
model = sm.OLS(y, X)
results = model.fit()
alpha = results.params[0]  # 截距 (常数项)
beta = results.params[1]   # 斜率 (rx 的系数)
x_line = np.array([rx.min(), rx.max()])
y_line = alpha + beta * x_line
#两点确定一条直线

ax.plot(x_line, y_line)
print(results.summary())
plt.show()
