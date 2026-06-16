import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

data=pd.read_excel("../data/hw13.1.xlsx")
print(data)
q=np.array(data["q"])
y=np.array(data['τ(q)'])

print(len(q))
def dif_toward_deg_one(x,y):
    dif=np.ones(len(x)-1)
    for i in range(len(x)-1):
        dif[i]=(y[i+1]-y[i])/(x[i+1]-x[i])
    return dif

def dif_backward_deg_one(x,y):
    dif=np.ones(len(x)-1)
    for i in range(1,len(x)-1):
        dif[i]=(y[i]-y[i-1])/(x[i]-x[i-1])
    return dif
def dif_center_deg_one(x,y):
    dif=np.ones(len(x)-2)
    for i in range(1,len(x)-1):
        dif[i-1]=(y[i+1]-y[i-1])/(x[i+1]-x[i-1])
    return dif

alpha=dif_toward_deg_one(q,y)
beta=dif_center_deg_one(q,y)
gamma=dif_backward_deg_one(q,y)

f1=q[0:len(q)-1:1]*alpha+y[0:len(y)-1]
f2=q[1:len(q):1]*gamma+y[1:len(y)]
f3=q[1:len(q)-1:1]*beta+y[1:len(y)-1]

print(f1.shape,f2.shape,f3.shape)

fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(q[0:len(q)-1:1],f2)
ax.plot(q[1:len(q):1],f2)
ax.plot(q[1:len(q)-1:1],f3)

ax.legend(["forward","backward","center"],loc="lower right")


fig.show()

