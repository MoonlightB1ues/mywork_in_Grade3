import numpy as np
data =np.array([
    [0.0879,   0.1570,  -0.0337,  0.4012,  -0.4543],
    [1.3519,   1.1652,  -0.7162,  0.9976,   0.9582],
    [0.1453,  -0.5307,   1.7220,  2.5578,   1.5265],
    [0.9401,   0.2823,  -0.6407,  1.3507,   0.8011],
    [-0.1272, -0.2282,  -0.9515, -0.8086,   0.2079],
    [0.0315,   0.0774,  -0.4331, -1.1469,  -0.2192],
    [-0.0429, -0.0814,  -0.5059,  0.1277,  -0.0914],
    [-0.0386, -0.1896,   1.1931,  1.4154,   0.8285],
    [0.2766,   0.3148,  -0.2917, -0.2753,  -0.2100]
])
index_change=1e-2*data
index_change=index_change.T
cov_matrix = np.cov(index_change, rowvar=False)  #认为每一行是不同个体的数据
corr_matrix = np.corrcoef(index_change, rowvar=False)
#print("协方差矩阵为：",cov_matrix.shape)
#print("相关系数矩阵为：",corr_matrix)
diag = np.diag(cov_matrix)
#print("对角线元素为：",diag)
tri_up=np.triu(cov_matrix,0) #参数0表示取不取对角元素,如果不取,可以命为-1
print(tri_up)
tri_down=np.tril(corr_matrix)
print(tri_down)
trace=np.trace(cov_matrix)
print(trace)

trace1=np.trace(corr_matrix)
print("相关系数矩阵的迹：",trace1)