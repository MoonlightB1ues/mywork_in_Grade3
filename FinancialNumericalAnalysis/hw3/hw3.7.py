import numpy as np
arr=np.random.randint(10,101,size=(20,20))
print(arr)
for i in range(20):
    for j in range(20):
        if arr[i,j]>80:
            arr[i,j]=110
print(arr)
d=arr[3:8,:]
print("\nd=",d)