import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from pandas.core.interchange.dataframe_protocol import DataFrame
from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
def equation(y):
    z=9.8-0.27/70*y**2
    return z


def Eulersolve(a,b,h): #a,b为初值,h为步长,欧拉向前法
    n = round((b-a)/h)
    y = np.zeros(n+1)
    y[0]=0#初值在这里设置一下
    x = np.arange(a,b+h,h)
    for i in range(1,len(y)):
        y[i] = y[i-1]+h*equation(y[i-1])    #显式方程
    return x,y

def Eulersolve_backwards(a,b,h): #a,b为初值,h为步长,欧拉向后法
    n = round((b-a)/h)
    y = np.zeros(n+1)   #初值在这里设置一下
    x = np.arange(a,b+h,h)
    m=70
    c=0.27
    g=9.8
    A = c ** 2 * h / m
    for i in range(1,len(y)):
        y[i] = (-1+(1+4*(c*h/m*(y[i-1]+h*g)))**0.5)/(2*c*h)*m #隐式方程
    return x,y

x,y = Eulersolve(0,20,0.1)
x1,y1 = Eulersolve_backwards(0,20,0.1)
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(x,y)
ax.plot(x,y1)
fig.show()