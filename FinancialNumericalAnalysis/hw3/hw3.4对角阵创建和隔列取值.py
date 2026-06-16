import numpy as np
arr=np.arange(1,17).reshape(4,4)
print(arr)
mask1=np.array([1,0,0,1],dtype=bool)
mask2=np.array([1,0,0,1],dtype=bool)
b=arr[1:3,1:3]
print(b)
submatrix = arr[np.ix_([0, 3], [0, 3])] #隔一列取数组
submatrix1 = arr[(0,3),(0,3)]
print(submatrix1)


dd=np.diag(arr)
dd1=np.diag(dd)  #取对角元素阵
print(dd1)