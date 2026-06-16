import numpy as np
from numpy.linalg import solve
a=np.array([2,-3,0,2,1,5,2,1,3,-1,1,-1,4,1,2,2]).reshape(4,4)
b=np.array([8,2,7,12]).reshape(4,1)
x=solve(a,b)
print(x)