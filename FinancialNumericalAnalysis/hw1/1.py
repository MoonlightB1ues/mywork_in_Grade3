import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data=pd.read_excel("data/金融计量4.xlsx")
data["fixin"]="1"
n=0
for i in range(0,60):
    if i%3==0:
        data.loc[n, "fixin"] = data.loc[i, "固定资产投资额累计增长(%)"]
        n+=1

n=0
data["M2"]="1"
for i in range(0,60):
    if i%3==0:
        data.loc[n, "M2"] = (data.loc[i,'货币和准货币(M2)供应量期末值(亿元)']+data.loc[i+1, '货币和准货币(M2)供应量期末值(亿元)']+data.loc[i+2, '货币和准货币(M2)供应量期末值(亿元)'])/3
        n+=1

data.to_excel("eco.xlsx",index=False)

print(data)
print(data.columns)

