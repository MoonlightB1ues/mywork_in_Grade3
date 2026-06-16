import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from pandas.core.interchange.dataframe_protocol import DataFrame
from sqlalchemy.dialects.postgresql.base import IDX_USING

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
def M_stable(M,n,r):  # 等额本金 保持要还的本金随时间线性减少,因此每期还款金额不同  M为本金,n为年限,r为年利率,向前欧拉法
    Loan=np.ones(n+1)
    Loan[0]=M
    t=np.arange(0,n+1,1)
    for i in range(1,n+1):
        Loan[i]=Loan[i-1]-M/n
    return t,Loan

def P_stable(M,n,r):  #等额本息法,保持还的钱随时间保持不变   M为本金,n为年限,r为年利率,向前欧拉法
    Loan=np.ones(n+1)
    Loan[0]=M
    p=M*r*(1+r)**n/((1+r)**n-1)
    t=np.arange(0,n+1,1)
    for i in range(1,n+1):
        Loan[i]=Loan[i-1]*(1+r)-p
    return t,Loan

x,y=M_stable(100,30,0.0325)
a,b=P_stable(100,30,0.0325)

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(x,y,'o-',label='$M_stable$')
ax.plot(a,b,'o-',label='$P_stable$')
ax.legend(loc='best')
plt.show()

