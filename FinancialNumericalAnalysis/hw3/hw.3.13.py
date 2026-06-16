import numpy as np
amazon=np.array([1822.68,1840.12,1871.15,1907.57,1869])
apple=[185.72,188.66,190.92,190.08,189.00]
apple=np.array(apple)
data = np.array([
    [1822.68, 1840.12, 1871.15, 1907.57, 1869.00],  # 亚马逊
    [185.72, 188.66, 190.92, 190.08, 189.00],       # 苹果
    [123.35, 124.73, 126.02, 128.93, 128.07],       # 微软
    [1136.59, 1124.86, 1170.80, 1184.50, 1168.78],  # 谷歌
    [345.26, 345.61, 354.99, 359.31, 354.45]        # 奈飞
])
print("数据类型为：",data.dtype)
print("数组形状为：",data.shape)
print("数组维度为：",data.ndim)
print("元素个数为：",data.size)

intarray=np.arange(0,26,1)
print(intarray)
applearray=np.linspace(185.72,189,40)
print(applearray)

array4_1=np.linspace(0,0,5)
print(array4_1)
array4_2=np.linspace(0,0,25).reshape(5,5)
print(array4_2)

