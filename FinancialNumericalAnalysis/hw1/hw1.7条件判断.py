import numpy as np
saple=0
saple+=100+500+200+800+300-200-500-400-300
print("3.29日时平安A股数量为：",saple)
returns=[0.019455, 0.004580, 0.011398, 0.004257, 0.004863]
hol=1
for i in returns:
    hol*=(1+i)
holvalue=77.10*hol*saple
print("4-8号收盘后市值为：",holvalue)
price=77.1
for i in returns:
    price+=price*i
testvalu=price*saple
print("测试市值为：",testvalu)
closing_prices = {75.35, 76.55, 75.80, 74.72, 72.29, 72.69, 74.22, 73.40, 77.10}
print("72.29是否属于：",72.29 in closing_prices)
print("75.81是否属于：",75.81 in closing_prices)
print("72.45是否属于：",72.45 in closing_prices)