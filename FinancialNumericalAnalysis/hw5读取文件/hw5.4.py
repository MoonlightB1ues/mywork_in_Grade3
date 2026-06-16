import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
data=pd.read_excel("data/hw5.4.xlsx")
data["日期"]=pd.to_datetime(data["日期"],format="%Y-%m-%d")
data.set_index("日期",inplace=True)

'''print(data.index,data.columns,data.shape)
print(data.loc["2020-04-08"])
print(data.loc["2020-05-18"])
print(data.loc["2020-06-10"])
print(data.loc["2020-06-15":"2020-06-19"])

print(data.iloc[16:29])
print(data.iloc[:,2:5])
'''
condition1=data["白云机场"]>=14.6
print(data.loc[condition1,:])

condition2=(data["华能国际"]<=6.6)&(data["南方航空"]>=5.5)&(data["三一重工"]<19.9)
print(data.loc[condition2,:])