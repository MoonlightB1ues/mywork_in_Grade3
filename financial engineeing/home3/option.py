import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import statsmodels.api as sm
from matplotlib import pyplot as plt
from scipy.stats import norm

class BSM:  #用类来封装代码

    def __init__(self, s,k,r,sigma,t):  #s为t时刻标的资产的价格,k为t时刻的行权价,r为无风险利率,sigma为隐含波动率,t为到期时间段,各参数为向量形式
        self.s = s
        self.k = k
        self.r = r
        self.sigma = sigma
        self.t = t

    def d1(self):
        d1=( np.log(self.s)-np.log(self.k)+(self.r+self.sigma**2/2)*self.t)/(np.power(self.t,0.5)*self.sigma)
        return d1

    def d2(self):
        d2=self.d1()-self.sigma*self.t**0.5
        return d2

    def call_price(self):
        c=self.s*norm.cdf(self.d1())-self.k*norm.cdf(self.d2())*np.power(np.e,-1*self.r*self.t)
        return c

    def put_price(self):
        p=self.k*norm.cdf(-1*self.d2())*np.pow(np.e,-1*self.r*self.t)-self.s*norm.cdf(-1*self.d1())
        return p

s=np.full(10,100)
k=np.full(10,95)
r=np.full(10,0.1)
sigma=np.full(10,0.3)
t=np.full(10,0.75)

s1=np.arange(95,105,1)

s1_BSM=BSM(s1,k,r,sigma,t)
s1_call=s1_BSM.call_price()
s1_put=s1_BSM.put_price()

k1=np.arange(95,105,1)
k1_BSM=BSM(s,k1,r,sigma,t)
k1_call=k1_BSM.call_price()
k1_put=k1_BSM.put_price()

r1=np.arange(0.05,0.15,0.01)
r1_BSM=BSM(s,k,r1,sigma,t)
r1_call=r1_BSM.call_price()
r1_put=r1_BSM.put_price()

si=np.arange(0.30,0.80,0.05)
si_BSM=BSM(s,k,r,si,t)
si_call=si_BSM.call_price()
si_put=si_BSM.put_price()

t1=np.arange(0.25,1.25,0.1)
t1_BSM=BSM(s,k,r,sigma,t1)
t1_call=t1_BSM.call_price()
t1_put=t1_BSM.put_price()

fig=plt.figure()
ax=fig.add_subplot(2,5,1)
ax.plot(s1,s1_call,label='s1_call')
ax.set_title("C-S")

ax1=fig.add_subplot(2,5,2)
ax1.plot(k1,k1_call,label='k1_call')
ax1.set_title("C-K")

ax2=fig.add_subplot(2,5,3)
ax2.plot(r1,r1_call,label='r1_call')
ax2.set_title("C-R")

ax3=fig.add_subplot(2,5,4)
ax3.plot(si,si_call,label='si_call')
ax3.set_title("C-sigma")

ax4=fig.add_subplot(2,5,5)
ax4.plot(t1,t1_call,label='t1_call')
ax4.set_title("C-T")


ax5=fig.add_subplot(2,5,6)
ax5.plot(s1,s1_put,label='s1_put')
ax5.set_title("P-S")

ax6=fig.add_subplot(2,5,7)
ax6.plot(k1,k1_put,label='t1_put')
ax6.set_title("P-T")

ax7=fig.add_subplot(2,5,8)
ax7.plot(r1,r1_put,label='r1_put')
ax7.set_title("P-R")

ax8=fig.add_subplot(2,5,9)
ax8.plot(si,si_put,label='si_put')
ax8.set_title("P-SI")

ax9=fig.add_subplot(2,5,10)
ax9.plot(t1,t1_put,label='t1_put')
ax9.set_title("P-T")


plt.tight_layout()
fig.show()


