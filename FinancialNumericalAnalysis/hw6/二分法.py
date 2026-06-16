import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def equation(x):
    f = 1000*((1+x/12)**480-1) - 5000*(1-(1+x/12)**(-240))  #定义目标函数f(x)
    return f
def bisection(a,b,e):  #定义二分法函数,a为初始下界,b为初始上界,e为误差容限
    c=(a+b)/2
    sign_fc=np.sign(equation(c))  #sign取函数值的正负号
    sign_fa=np.sign(equation(a))
    sign_fb=np.sign(equation(b))
    while b-c>e:
        if sign_fb*sign_fc<=0:   #若f(b)f(c)异号,则将取值范围缩小到(c,b)
            a=c
            sign_fa=sign_fc
        else:
            b=c
            sign_fb=sign_fc
        c=(a+b)/2
        sign_fc=np.sign(equation(c))
    root=c
    return root
print(bisection(0,2.0,1e-5))