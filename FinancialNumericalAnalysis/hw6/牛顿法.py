import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def equation(x):
    f=x**4-5.4*x**3+10.56*x**2-8.954*x+2.7951
    return f

def equation_diff(x):
    df=4*x**3-5.4*3*x**2+10.56*2*x-8.954
    return df



def newton(x0,e):
    f=equation(x0)
    df=equation_diff(x0)
    x1=x0-f/df
    while abs(x1-x0)>e:
        x0=x1
        f=equation(x0)
        df=equation_diff(x0)
        x1=x0-f/df
    root=x1
    return root



for i in np.arange(1,1.2+0.01,0.01):
    print(newton(i,9.999999999999999999999e-6))