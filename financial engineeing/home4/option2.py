import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import statsmodels.api as sm
from matplotlib import pyplot as plt
from scipy.stats import norm
from scipy.optimize import brentq
from scipy.optimize import newton

data_5 = pd.read_excel('期权价格.xlsx',sheet_name=0)
data_6 = pd.read_excel('期权价格.xlsx',sheet_name=1)
data_7 = pd.read_excel('期权价格.xlsx',sheet_name=2)
data_8 = pd.read_excel('期权价格.xlsx',sheet_name=3)
d0 = pd.to_datetime('2026-05-06')
d1 = pd.to_datetime('2026-05-27')
d2 = pd.to_datetime('2026-06-24')
d3 = pd.to_datetime('2026-09-23')
d4 = pd.to_datetime('2026-12-23')

data_5["t"]=(d1-d0).days/365
data_6["t"]=(d2-d0).days/365
data_7["t"]=(d3-d0).days/365
data_8["t"]=(d4-d0).days/365
data=pd.concat([data_5,data_6,data_7,data_8],axis=0,ignore_index=True)

data["r"]=0.0142
data["s"]=3.1
print(data)



r=data["r"]
s=data["s"]
t=data["t"]
k=data["行权价"]
c=data["认购期权"]
p=data["认沽期权"]


class BSM:  #用类来封装代码

    def __init__(self, s,k,r,t,c=None,p=None,sigma=None):  #s为t时刻标的资产的价格,k为t时刻的行权价,r为无风险利率,sigma为隐含波动率,t为到期时间段,各参数为向量形式
        self.s = s
        self.k = k
        self.r = r
        if sigma is None:
            self.sigma = np.full_like(s,0.1)
        else:
            self.sigma = sigma
        self.t = t
        self.p = p
        self.c = c

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
        p=self.k*norm.cdf(-1*self.d2())*np.power(np.e,-1*self.r*self.t)-self.s*norm.cdf(-1*self.d1())
        return p


    def implied_volatility_call(self):
        guess = np.full_like(self.s, 0.2)
        # 1. 你定义了一个函数给 fsolve
        def objective_function(sigma_guess):
            # 2. fsolve 盲目地传进来一个数组，比如 [0.2]
            # 你在这里做了一个“偷梁换柱”的动作！
            # 你把 fsolve 瞎猜的数字，赋值给了你类里面的 self.sigma
            self.sigma = sigma_guess
            # 3. 然后你调用理论定价公式
            # 注意：此时的 self.call_price() 内部用到的是刚才被覆盖的新 self.sigma！
            theory_price = self.call_price()
            # 4. 返回误差给 fsolve
            return theory_price - self.c
        # 5. fsolve 登场
        # 它只知道：我调用 objective_function，并不断修改传进去的参数
        # 直到它返回 0
        result=newton(objective_function,guess)  #传guess进sigma_guess
        return result

    def implied_volatility_put(self):
        guess = np.full_like(self.s, 0.2)
        # 1. 你定义了一个函数给 fsolve
        def objective_function(sigma_guess):
            # 2. fsolve 盲目地传进来一个数组，比如 [0.2]
            # 你在这里做了一个“偷梁换柱”的动作！
            # 你把 fsolve 瞎猜的数字，赋值给了你类里面的 self.sigma
            self.sigma = sigma_guess
            # 3. 然后你调用理论定价公式
            # 注意：此时的 self.call_price() 内部用到的是刚才被覆盖的新 self.sigma！
            theory_price = self.put_price()
            # 4. 返回误差给 fsolve
            return theory_price - self.p
        # 5. fsolve 登场
        # 它只知道：我调用 objective_function，并不断修改传进去的参数
        # 直到它返回 0
        result=newton(objective_function,guess)  #传guess进sigma_guess
        return result

cal=BSM(s,k,r,t,c=c,p=p,sigma=None)
inv_call=cal.implied_volatility_call()
inv_put=cal.implied_volatility_put()

data_put=pd.DataFrame({'k':k,'inv':inv_put})
data_call=pd.DataFrame({'k':k,'inv':inv_call})
data_inv=pd.concat([data_put,data_call],axis=0,ignore_index=True)
print(data_inv)

coefficients = np.polyfit(data_inv["k"],data_inv["inv"], 2)
print("拟合得到的系数 [a, b, c]:", coefficients)
# np.poly1d 会把这三个系数变成一个可以直接调用的数学函数！
fit_function = np.poly1d(coefficients)
print("\n具体的拟合方程为:\n", fit_function)
x=np.linspace(0,6,20)
y=fit_function(x)


fig=plt.figure()
ax1=fig.add_axes([0.1,0.1,0.8,0.8])
ax1.plot(x,y)
plt.show()