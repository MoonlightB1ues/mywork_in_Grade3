import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from pandas.core.interchange.dataframe_protocol import DataFrame
from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})


def equation2(x):
    z=-1000*x + 200
    return z
def zoid(a,b,h): #a,b为初值,h为步长,longge-梯形法
    n = round((b-a)/h)    #转换为整型
    y = np.zeros(n+1)   #n份自然有n+1个点
    y[0]=0  #初值在这里设置一下
    x = np.arange(a,b+h,h)
    for i in range(1,len(y)):
        y[i] = (0.95*y[i-1]+0.02)/1.05
    return x,y

def rk_midpoint(a,b,h): #a,b为初值,h为步长,rk-中点法  rk法用起来狠方便,直接复制这一串,然后改一下equation2
    n = round((b-a)/h)
    y = np.zeros(n+1)
    x = np.arange(a,b+h,h)
    for i in range(n):
        k1 = equation2(y[i])
        k2 = equation2(y[i] + h*k1/2)
        y[i+1] = y[i] + h*k2
    return x,y


def rk_trapezoid(a,b,h):    #rk-梯形法
    n = round((b-a)/h)
    y = np.zeros(n+1)
    x = np.arange(a,b+h,h)
    for i in range(n):
        k1 = equation2(y[i])
        k2 = equation2(y[i] + h*k1)
        y[i+1] = y[i] + h*(k1 + k2)/2
    return x,y

x,y = zoid(0,0.02,0.0001)
x1,y1 = rk_trapezoid(0,0.02,0.0001)
x2,y2 = rk_midpoint(0,0.02,0.0001)
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(x1,y1,label="rk_zoid")
ax.plot(x,y,label="zoid")
ax.plot(x2,y2,label="rk midpoint")
ax.legend()
plt.show()
