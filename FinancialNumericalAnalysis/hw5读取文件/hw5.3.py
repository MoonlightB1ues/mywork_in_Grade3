import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
data=pd.read_excel("../data/上证50.xlsx")
data["成交金额(亿元)_TrdSum"] = data["成交金额(元)_TrdSum"] / 100000000
data["交易日期_TrdDt"]=pd.to_datetime(data["交易日期_TrdDt"],format='%Y-%m-%d')

'''fig1=plt.figure()
ax=fig1.add_axes([0.1,0.1,0.8,0.8])
ax.plot(data["交易日期_TrdDt"],data["涨跌幅(%)_ChgPct"])
ax.set_xticks(ticks=pd.to_datetime(["2018-01","2018-08","2019-03","2019-10","2020-04","2020-09"],format='%Y-%m'),
              labels=["2018-01","2018-08","2019-03","2019-10","2020-04","2020-09"],fontsize=12)

fig2=plt.figure()
ax2=fig2.add_axes([0.1,0.1,0.8,0.8])
ax2.hist(data["成交金额(亿元)_TrdSum"],bins=100)
'''

'''fig3=plt.figure()
ax3=fig3.add_axes([0.1,0.1,0.8,0.8])
data["时间周期"] = data["交易日期_TrdDt"].dt.to_period("M")
data["时间周期"] = data["时间周期"].dt.to_timestamp("M")
sns.boxplot(
    x=data["时间周期"],  # x轴：时间周期（年月）
    y=data["成交金额(亿元)_TrdSum"],  # y轴：成交金额
    palette="Set2",  # 箱体颜色
)
ax3.xaxis.set_major_locator(plt.MaxNLocator(4))
'''
print(data.columns)
fig4=plt.figure()
ax4=fig4.add_subplot(2,2,1)
ax4.plot(data["交易日期_TrdDt"],data["开盘价(元/点)_OpPr"])
plt.gca().set_xticks(ticks=pd.to_datetime(["2018-01","2018-12","2019-10","2020-09"],format='%Y-%m'),
              labels=["2018-01","2018-12","2019-10","2020-09"],fontsize=12)
plt.gca().set_yticks(ticks=[2500,3000,3500],labels=["2500","3000","3500"],fontsize=12)
ax5=fig4.add_subplot(2,2,2)
ax5.plot(data["交易日期_TrdDt"],data["最高价(元/点)_HiPr"])
plt.gca().set_xticks(ticks=pd.to_datetime(["2018-01","2018-12","2019-10","2020-09"],format='%Y-%m'),
              labels=["2018-01","2018-12","2019-10","2020-09"],fontsize=12)
plt.gca().set_yticks(ticks=[2500,3000,3500],labels=["2500","3000","3500"],fontsize=12)
ax6=fig4.add_subplot(2,2,3)
ax6.plot(data["交易日期_TrdDt"],data["最低价(元/点)_LoPr"])
plt.gca().set_xticks(ticks=pd.to_datetime(["2018-01","2018-12","2019-10","2020-09"],format='%Y-%m'),
              labels=["2018-01","2018-12","2019-10","2020-09"],fontsize=12)
plt.gca().set_yticks(ticks=[2500,3000,3500],labels=["2500","3000","3500"],fontsize=12)
ax7=fig4.add_subplot(2,2,4)
ax7.plot(data["交易日期_TrdDt"],data["收盘价(元/点)_ClPr"])
plt.gca().set_xticks(ticks=pd.to_datetime(["2018-01","2018-12","2019-10","2020-09"],format='%Y-%m'),
              labels=["2018-01","2018-12","2019-10","2020-09"],fontsize=12)
plt.gca().set_yticks(ticks=[2500,3000,3500],labels=["2500","3000","3500"],fontsize=12)
plt.show()