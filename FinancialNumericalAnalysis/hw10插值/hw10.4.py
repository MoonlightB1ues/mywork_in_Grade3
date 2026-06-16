import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def Interp_Newton(x, fx, xval):
    N = len(x)
    duoxiangshi = np.ones([len(xval), N]) # 给每个函数项赋初值
    chashang = np.zeros([N, N+1])            # 给差商赋初值
    chashang[:, 0] = x
    chashang[:, 1] = fx
    for i in range(2, N+1):
        chashang[i-1:, i] = (chashang[i-1:, i-1] - chashang[i-2:-1, i-1]) / (chashang[i-1:, 0] - chashang[0:-1-i+2, 0])
        duoxiangshi[:, i-1] = duoxiangshi[:, i-2] * (xval - x[i-2])
    table_cs = chashang[1:, 2:]                   #得出差商表
    chashang = chashang[:, 1:]
    newton_xishu = np.diag(chashang)      #得出牛顿系数项,就是差商表的对角元素
    yval = np.zeros(len(xval))
    for i in range(len(xval)):
        yval[i] = np.sum(duoxiangshi[i, :] * newton_xishu) #得出该多项式在每一点的函数值
    return table_cs, newton_xishu, yval

i=np.arange(0.4,0.9,0.01)
x=np.array([0.40,0.55,0.65,0.80,0.90,1.05])
y=np.array([0.41075,0.57815,0.69675,0.88811,1.02652,1.25382])
table_cs, newton_xishu, yval = Interp_Newton(x,y,i)
print(table_cs)
fig=plt.figure(1)
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(i,yval)
plt.show()
