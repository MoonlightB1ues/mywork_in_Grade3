import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data = pd.read_table('../data/Exp04-Python-实验数据-余额宝历史收益.txt', sep=r'\s+', encoding='GB2312')
stock_time = pd.to_datetime(data['日期'][-1::-1], format='%Y-%m-%d')
stock_time.reset_index(drop=True, inplace=True)
stock_revenue = data['七日年化收益率%'][-1::-1]
stock_revenue.reset_index(drop=True, inplace=True)
stock_gain = data['万份收益'][-1::-1]
stock_gain.reset_index(drop=True, inplace=True)

data['日期'] = stock_time  # 替换为转换后的日期格式
data['七日年化收益率%'] = stock_revenue  # 替换为反转后的收益率
data['万份收益'] = 0.01*stock_gain  # 替换为反转后的万份收益

data = data.drop(columns=['七日年化收益率%'])



data['资产累计'] =1.0


for i in range(17, len(data)):
    # 第i行资产 = 第i-1行资产 * (1 + 第i-1行收益率)
    data.loc[i, '资产累计'] = data.loc[i-1, '资产累计'] * (1 + data.loc[i-1, '万份收益'])**((data.loc[i,'日期']-data.loc[i-1,'日期']).days)

target_time = pd.to_datetime('2013-06-18')


