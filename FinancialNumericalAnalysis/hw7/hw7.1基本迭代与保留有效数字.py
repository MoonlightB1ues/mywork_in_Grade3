import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})


def f(x):
    y=(0.8+x**2)**(1/3)
    return y

def ite(x,e):   # x为初值,e为误差 迭代求根
    y = f(x)
    z = f(y)
    while z-y>e:
        y = f(z)
        z = f(y)
    return z


z=ite(2,0.00001)
print(f"{z:.4g}")   #保留四位有效数字
print(z)