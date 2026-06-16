import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def myfun_integral_fun(x):
    f =np.pow(1+np.exp(x),0.5)
    return f


def myfun_integral_simpson(a, b, n):
    x_0 = a
    x_n = b
    h = (x_n - x_0)/n
    xp = np.arange(a, b+h, h)
    fxp = myfun_integral_fun(xp)
    fxp[1:-1:2] = fxp[1:-1:2]*4
    fxp[2:-1:2] = fxp[2:-1:2]*2
    print("fxp ", fxp)
    Sn = np.sum(fxp)*h/3
    return Sn


data = pd.DataFrame(0, index=range(9), columns=["n", "F", "Error","Ratio"])  #要生成多个n的表
data["Ratio"]=1
data["n"]=np.logspace(1,9,9,base=2)
for i in range(9):
    data.loc[i,"F"]=myfun_integral_simpson(0,2,data.loc[i,"n"])
data["Error"]=4.006994-data["F"]
data["Ratio"]=data["Error"]/data["Error"].shift(1)
print(data)

