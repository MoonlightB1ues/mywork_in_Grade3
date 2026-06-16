import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def f(x):
    f=x**4-5.4*x**3+10.56*x**2-8.954*x+2.7951
    return f
def df(x):
    df=4*x**3-5.4*x**2*3+10.56*x*2-8.954
    return df

def newton(x0,e):
    y0=f(x0)
    dy0=df(x0)
    x1=x0-y0/dy0
    while abs(x1-x0)>e:
        x0=x1
        y0=f(x0)
        dy0=df(x0)
        x1=x0-y0/dy0
    root=x1
    return root

print(newton(1.05,0.0001))