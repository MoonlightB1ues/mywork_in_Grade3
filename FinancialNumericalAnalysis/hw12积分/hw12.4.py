import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data=pd.read_excel("../data/Exp12-Python-实验数据-对数正态分布数据样本.xlsx")
miu=np.average(np.log(data["数据样本"]))
sigma=np.std(np.log(data["数据样本"]))
print(miu,sigma)


def myfun_integral_fun(x):
    f =np.exp(np.pow((np.log(x))-miu,2)*(-1)/(2*sigma*sigma))/(sigma*x*np.pow(2*np.pi,0.5))
    return f

def myfun_integral_simpson(a, b, n):
    x_0 = a+1e-5
    x_n = b
    h = (x_n - x_0)/n
    xp = np.arange(x_0, x_n+h, h)
    fxp = myfun_integral_fun(xp)
    fxp[1:-1:2] = fxp[1:-1:2]*4
    fxp[2:-1:2] = fxp[2:-1:2]*2
    Sn = np.sum(fxp)*h/3
    return Sn

fx=myfun_integral_fun(np.array([0.0001]))
print(fx)

Sn=1-myfun_integral_simpson(0.000000001,5,50000)
print("区间分成50000份的生存函数值:",Sn)
Sn=1-myfun_integral_simpson(0.000000001,5,10)
print("区间分成10份的生存函数值:",Sn)