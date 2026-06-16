import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as scio
from scipy.stats import norm
def myfun_LSQ(Xi, Yi):
    n = len(Xi)
    sumXi = np.sum(Xi)
    sumXi2 = np.sum(Xi**2)
    sumYi = np.sum(Yi)
    sumXiYi = np.sum(Xi*Yi)
    A = np.array([[n, sumXi], [sumXi, sumXi2]])
    b = np.array([[sumYi], [sumXiYi]])
    ParLSQ = np.dot(np.linalg.inv(A), b)
    return ParLSQ
Xi = np.arange(-1,1+0.1,0.1)
Yi = np.array([1.032,
1.563,
1.614,
1.377,
1.179,
1.189,
0.910,
1.139,
0.646,
0.474,
0.418,
0.067,
0.371,
0.183,
-0.415,
-0.112,
-0.817,
-0.234,
-0.623,
-0.536,
-1.173
])
ParLSQ = myfun_LSQ(Xi, Yi)
b = ParLSQ[0]
m = ParLSQ[1]
x = np.arange(-1,1+0.1,0.1)
y = m*x+b
plt.plot(Xi, Yi, 'ro')
plt.plot(x, y, 'b-', lw=2)
plt.show()