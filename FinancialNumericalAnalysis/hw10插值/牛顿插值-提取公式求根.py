import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
X=np.array([0.0025, 0.005, 0.0075,0.01, 0.0125, 0.015, 0.0175])

def equation(x):
    f=(894+30.56)+(894+30.56)/(1+x)+(894+30.56)/np.power(1+x, 2)+(894+30.56)/np.power(1+x, 3)+(894+30.56)/np.power(1+x, 4)+(894+30.56)/np.power(1+x, 5)-5361.74
    return f
y=equation(X)
def newton(x, fx, xval):
    N = len(x)
    duoxiangshi = np.ones([len(xval), N]) # 给每个函数项赋初值
    chashang = np.zeros([N, N+1])            # 给差商赋初值
    chashang[:, 0] = x
    chashang[:, 1] = fx
    for i in range(2, N+1):
        chashang[i-1:, i] = (chashang[i-1:, i-1] - chashang[i-2:-1, i-1]) / (chashang[i-1:, 0] - chashang[0:-1-i+2, 0])
        duoxiangshi[:, i-1] = duoxiangshi[:, i-2] * (xval - x[i-2])
    table_cs = chashang[1:, 2:]                   #得出差商表
    chashang = chashang[:, 1:]
    newton_xishu = np.diag(chashang)      #得出牛顿系数项
    yval = np.zeros(len(xval))
    for i in range(len(xval)):
        yval[i] = np.sum(duoxiangshi[i, :] * newton_xishu) #得出该多项式在每一点的函数值
    return newton_xishu

newton_xishu=newton(X,y,np.array([1,2,3,4.0]))


def equation1(z):    #x为已有插值点
    n=len(X)
    duoxiangshi = np.ones(n)
    for i in range(1,n):
        duoxiangshi[i] = duoxiangshi[i-1] * (z-X[i-1])
    y=np.sum(duoxiangshi[:] * newton_xishu)
    return y

def bisection(a,b,e):
    c=(a+b)/2
    sign_fc=np.sign(equation(c))
    sign_fa=np.sign(equation(a))
    sign_fb=np.sign(equation(b))
    while b-c>e:
        if sign_fb*sign_fc<=0:
            a=c
            sign_fa=sign_fc
        else:
            b=c
            sign_fb=sign_fc
        c=(a+b)/2
        sign_fc=np.sign(equation(c))
    root=c
    return root

def bisection1(a,b,e):
    c=(a+b)/2
    sign_fc=np.sign(equation1(c))
    sign_fa=np.sign(equation1(a))
    sign_fb=np.sign(equation1(b))
    while b-c>e:
        if sign_fb*sign_fc<=0:
            a=c
            sign_fa=sign_fc
        else:
            b=c
            sign_fb=sign_fc
        c=(a+b)/2
        sign_fc=np.sign(equation(c))
    root=c
    return root


a=bisection(0,0.2,1e-7)
print(a)



root=bisection1(0,0.2,1e-6)

print(root)