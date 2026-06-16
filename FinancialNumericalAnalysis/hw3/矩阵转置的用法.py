import numpy as np
b=np.array([1,2,-3,2,0,1,2,-3,0,0,1,2,0,0,0,1]).reshape(4,4)
print(b)
c=np.array([1,2,0,1,0,1,2,0,0,0,1,2,0,0,0,1]).reshape(4,4)
print(c)
a=np.linalg.inv(2*np.eye(4)-np.linalg.inv(c)@b)@np.linalg.inv(c)
print(a.T)