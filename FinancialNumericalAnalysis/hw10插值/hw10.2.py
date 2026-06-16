import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
def interpolation(x,y,z):
    n=len(x)
    fx = np.zeros_like(z, dtype=np.float64)
    k=np.zeros(n)
    for i in range(n):  # 遍历每一个K
        f=1
        q = np.ones_like(z, dtype=np.float64)
        for j in chain(range(i), range(i+1, n)):
            f*=x[i]-x[j]
            q*=z-x[j]
        fx+=y[i]/f*q
    return fx

x=np.array([1,2])
y=np.exp(x)
z=np.arange(0,3+0.01,0.01)
fx=np.exp(z)-interpolation(x,y,z)
fig=plt.figure(1)
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(z,fx)
plt.show()