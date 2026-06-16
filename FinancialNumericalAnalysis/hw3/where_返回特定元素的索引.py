import numpy as np

data = np.array([
    [13.0709, 12.117,   12.6708,   3.4179,  -20.7889,   0.6729],   # 阿里健康
    [33.6957,  6.7551,  12.4365, -13.3183,   -8.3333,  -7.5284],   # 平安好医生
    [10.1911, -2.948,    7.5045,   7.4792,  -15.9794,   8.1595],   # 腾讯控股
    [-23.839, 21.5447,  -4.8495,   5.6239,  -20.2995,   4.3841],   # 小米集团
    [21.4123, 14.2589, -13.1363,   7.7505,    6.2281,  13.1396]    # 美团点评
])

print(data[0,1])
print(data[2,2])
print(data[4,5])

index1=np.where(data>10)
print(index1)
value1=data[index1]
print(value1)

index2=np.where(data<-15)
print(index2)
value2=data[index2]
print(value2)

print("小米集团：",data[3,:])
print("5月涨幅：",data[:,4])
print("平安好医生",data[1,1:4])
print("腾讯控股",data[2,1:4])

data1=np.sort(data,axis=1)  #横轴排序
print(data1)
data2=np.sort(data,axis=0)  #竖轴排序
print(data2)
