import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from envs.my_pythorch.Lib.unittest.mock import inplace
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
data=pd.read_csv("../data/hw5.5.csv", sep=",", encoding='GB2312')
#print(data.head())
data.set_index("交易日期", inplace=True)
data=data.pivot_table(     # 类似excel中数据透视表的效果,好用!
    index="交易日期",  # 要转为行标的列
    columns="指数名称",  # 要转为列标的列（可选）
    values="收盘价"  # 填充到表格中的值
)
#print(data.head())
print(np.where(data.isnull()),data.shape)

data.drop(data.index[[3,13]],inplace=True)
print(data.head())
print(np.where(data.isnull()),data.shape)

data.fillna(method="ffill",inplace=True)
print(data)

data.fillna(method="bfill",inplace=True)
print(data)