import numpy as np
a=np.random.randn(100,100)
for i in range(100):
    if a[9,i]<0:
        a[9,i]=-0.5
for i in range(100):
    if a[54,i]<0:
        a[54,i]=-0.5
for i in range(100):
    if a[i,17]<0:
        a[i,17]=-0.5
for i in range(100):
    if a[i,76]<0:
        a[i,76]=-0.5
a=np.delete(a,24,0)
a=np.delete(a,56,0)
a=np.delete(a,37,1)
a=np.delete(a,72,1)
print(a)