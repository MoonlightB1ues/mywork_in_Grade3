import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def equation(x,y):
    z=2/3*x*y**(-2)
    return z


def Eulersolve(a,b,h): #a为初值,这是向前欧拉法
    n = round((b-a)/h)
    y = np.ones(n+1)
    x = np.arange(a,b+h,h)
    for i in range(0,len(y)-1):
        y[i+1] = y[i]+h*equation(x[i],y[i])
    return x,y


x,y = Eulersolve(0,1.2,0.05)
fx=np.pow((1+np.pow(x,2)),1/3)

fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(x,y,label="Eulervalue")
ax.plot(x,fx,label="Truevalue")
ax.legend()
plt.show()

err=np.abs(y-fx)
err_ratio=np.zeros_like(y)
err_ratio[1:]=err[0:-1]/err[1:]
data=pd.DataFrame({'truevalue':fx,'Eulervalue':y,"err":err,'err_ratio':err_ratio})
data=data.drop(index=0)
data.reset_index(inplace=True)
print(data)