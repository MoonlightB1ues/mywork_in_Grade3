import numpy as np
arr=np.arange(1,17).reshape(4,4)
print(arr)
arr[0,0]=0
print("\n",arr)
arr[1,1]=arr[0,1]+arr[1,0]
print("\n",arr)