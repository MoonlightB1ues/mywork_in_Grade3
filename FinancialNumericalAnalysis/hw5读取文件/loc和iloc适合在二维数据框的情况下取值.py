import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

#data=pd.read_excel("data/hw5.2.xlsx")
a=np.random.randint(1,10,81).reshape(9,9)
#print(a)
data=pd.DataFrame(a)
data1=data.iloc[0:5,:]
# print(data1)
data2=data.iloc[-6:-1,:]
print(data2)
data4=data[-6:-1]
print(data4)

#np.random.randint(10,10)
# print(data3)

# data1.to_excel("data/hw5.2.1.xlsx")
# data2.to_csv("data/hw5.2.2.csv")
# data3.to_csv("data/hw5.2.3.txt")