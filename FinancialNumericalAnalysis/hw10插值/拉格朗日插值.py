import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})


x=np.array([0.0,1.0,2.0,3.0,4.0,5.0,6.0])
y=np.array([2.0000,2.1592,3.1697,5.4332,9.1411,14.406,21.303])
k=np.zeros_like(y)
k[0]=y[0]/((x[0]-x[1])*(x[0]-x[2])*(x[0]-x[3])*(x[0]-x[4])*(x[0]-x[5]))
def interpolation(x,y,z):   #x是插值点,y是插值点的值,z是我要预测的点
    n=len(x)
    fx = np.zeros_like(z, dtype=np.float64)  #fx是我选定点预测的值
    for i in range(n):  # 遍历每一个K
        f=1
        q = np.ones_like(z, dtype=np.float64)  #f和q是基函数的一部分
        for j in chain(range(i), range(i+1, n)):
            f*=x[i]-x[j]
            q*=z-x[j]
        fx+=y[i]/f*q
    return fx

z=np.arange(0,6+0.01,0.01)
y=interpolation(x,y,z)

fig=plt.figure(1)
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(z,y)
plt.show()