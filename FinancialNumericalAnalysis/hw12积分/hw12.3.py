import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data=pd.read_csv("../data/RESSET_IDXWKRET_1.csv", sep=",")
data=data.dropna()
miu=np.average(data["IdxWkRet"])
sigma=np.std(data["IdxWkRet"])

def myfun_integral_fun(x):
    f =np.exp(np.pow(x-miu,2)*(-1)/(2*sigma**2))/(sigma*np.pow(2*np.pi,0.5))
    return f

def myfun_integral_simpson(a, b, n):
    x_0 = a
    x_n = b
    h = (x_n - x_0)/n
    xp = np.arange(x_0, x_n+h, h)
    fxp = myfun_integral_fun(xp)
    fxp[1:-1:2] = fxp[1:-1:2]*4
    fxp[2:-1:2] = fxp[2:-1:2]*2
    Sn = np.sum(fxp)*h/3
    return Sn

Tn = myfun_integral_simpson(-0.12, 0.12, 1000)
print(Tn)
