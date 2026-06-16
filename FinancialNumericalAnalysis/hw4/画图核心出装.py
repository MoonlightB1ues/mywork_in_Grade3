import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data = pd.read_table('../data/Exp04-Python-实验数据-600000_2012-12-18.txt', sep=',', encoding='GB2312') #读txt文件时的标准格式
data.columns = data.columns.str.strip()  #去除标题可能存在的空格
print(data.head())
stock_time = pd.to_datetime(data['成交时间'][-1::-1], format='%H:%M:%S')

stock_time.reset_index(drop=True, inplace=True) #替代时间原有的索引列
print(data.head())
stock_price = data['成交价'][-1::-1] #把价格倒过来
stock_price.reset_index(drop=True, inplace=True) #也把价格的索引替代掉
stock_volume = data['成交量(手)'][-1::-1]
stock_volume.reset_index(drop=True, inplace=True)

noon_time = pd.to_datetime('12:00:00', format='%H:%M:%S')  #定义上下午
ind_morning = stock_time < noon_time   #返回的是一个布尔序列
ind_afternoon = stock_time > noon_time

plt.figure(1)
plt.axes([.2, .52, .7, .4])
plt.plot(stock_time[ind_morning], stock_price[ind_morning], '-k', lw=0.5)
plt.plot(stock_time[ind_afternoon], stock_price[ind_afternoon], '-m', lw=0.5)
plt.plot(pd.to_datetime(['09:30', '15:00'], format='%H:%M'), [9.07, 9.07], '-r', lw=2)
plt.xlim(pd.to_datetime(['09:30', '15:00'], format='%H:%M'))
plt.xticks(ticks=pd.to_datetime(['09:30', '10:30', '11:30', '13:00', '14:00', '15:00'], format='%H:%M'),
          labels=[], #使自变量不显示标签
          fontsize=18)
plt.yticks(ticks=np.arange(8.9, 9.4, 0.1), fontsize=18)
plt.ylabel(r'$p$', fontsize=24)
plt.text(pd.to_datetime('11:00', format="%H:%M"), 9.02, 'close price on Dec 17, 2012', fontsize=18)
plt.title('The transaction history of 600000 on Dec 18, 2012', fontsize=15)

plt.axes([.2, .2, .7, .27])
plt.plot(stock_time.loc[ind_morning], stock_volume[ind_morning], '-c', lw=0.5)
plt.plot(stock_time.loc[ind_afternoon], stock_volume[ind_afternoon], '-b', lw=0.5)
plt.xlim(pd.to_datetime(['09:30', '15:00'], format='%H:%M'))
plt.xticks(ticks=pd.to_datetime(['09:30', '10:30', '11:30', '13:00', '14:00', '15:00'], format='%H:%M'),
          labels=['09:30', '10:30', '11:30', '13:00', '14:00', '15:00'],
          fontsize=18)
plt.xlabel(r'$t$', fontsize=24)
plt.yticks(ticks=np.arange(0, 30001, 10000),
           labels=[0, '1E4', '2E4', '3E4'],
           fontsize=18)
plt.ylabel(r'$v$', fontsize=24)
plt.show()
plt.savefig('Fig_600000_TranHis_20121218.jpg', dpi=300, bbox_inches='tight') #保存文件