import numpy as np
# ---------------------- 1. 求根方程设定【请补全此处代码】 ----------------------
# 定义目标函数f(x)，对应题目中的非线性方程
d=8421.21*0.06
k=8421.21/6
def equation(x):
    s = (d+k)/(1+x)+(d+k)/(1+x)
    return s

def bisection(a, b, e):
    c = (a + b) / 2
    sign_fc = np.sign(equation(c))  # sign取函数值的正负号
    sign_fa = np.sign(equation(a))
    sign_fb = np.sign(equation(b))
    while b - c > e:
        if sign_fb * sign_fc <= 0:  # 若f(b)f(c)异号,则将取值范围缩小到(c,b)
            a = c
            sign_fa = sign_fc
        else:
            b = c
            sign_fb = sign_fc
        c = (a + b) / 2
        sign_fc = np.sign(equation(c))
    root = c
    return root


print(bisection(0, 2.0, 1e-5))


