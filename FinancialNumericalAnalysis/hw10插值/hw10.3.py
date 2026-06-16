import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def aly(x,z):
    n = len(x)
    fx = np.ones_like(z, dtype=np.float64)
    for i in range(n):
        fx *= z-x[i]
    return fx

x1=np.array([1,2,3,4,5])
x2=np.array([1,2,3,4,5,6])
x3=np.array([1,2,3,4,5,6,6])
x4=np.array([1,2,3,4,5,6,7,8])
x5=np.array([1,2,3,4,5,6,7,8,9])


z1=np.arange(1,5+0.01,0.01)
z2=np.arange(1,6+0.01,0.01)
z3=np.arange(1,7+0.01,0.01)
z4=np.arange(1,8+0.01,0.01)
z5=np.arange(1,9+0.01,0.01)

y1=aly(x1,z1)
y2=aly(x2,z2)
y3=aly(x3,z3)
y4=aly(x4,z4)
y5=aly(x5,z5)

fig=plt.figure(1)
ax1=fig.add_subplot(2,3,1)
ax2=fig.add_subplot(2,3,2)
ax3=fig.add_subplot(2,3,3)
ax4=fig.add_subplot(2,3,4)
ax5=fig.add_subplot(2,3,5)


ax1.plot(z1,y1)
ax2.plot(z2,y2)
ax3.plot(z3,y3)
ax4.plot(z4,y4)
ax5.plot(z5,y5)
plt.show()

