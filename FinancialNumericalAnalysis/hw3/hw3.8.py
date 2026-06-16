import numpy as np
from numpy import ufunc

arr1=np.array([1/3,0,0,0,1/4,0,0,0,1/7]).reshape(3,3)
print(arr1)
arrb=np.linalg.inv(np.linalg.inv(arr1)-np.eye(3))*6
print(arrb)