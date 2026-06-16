import numpy as np
from numpy.ma.extras import average

print("保险理赔人数的期望：",1e4*0.06)
print("保险理赔人数的方差:",(1e4*0.06*0.94)**(1/2))
pay_person=np.random.binomial(1e4,0.06,100)  #二项分布
print(average(pay_person))
print(np.var(pay_person)**(1/2))

print("几何分布的期望为：",1/0.06)
print("几何分布的标准差为：",((1-0.06)/0.06**2)**(1/2))

pay_insurance=np.random.geometric(0.06, 200)  #几何分布
print(average(pay_insurance))
print(np.var(pay_insurance)**(1/2))