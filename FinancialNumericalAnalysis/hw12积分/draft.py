import pandas as pd
import numpy as np

A=np.array([3,-1,1,1,3,1,1,2,7]).reshape(3,3)
L=np.tril(A,-1)
U=np.triu(A,1)
print(A,U)