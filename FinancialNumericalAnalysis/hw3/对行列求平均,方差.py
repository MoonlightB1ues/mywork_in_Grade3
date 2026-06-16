import numpy as np

data = np.array([
    [11.0901, 11.2352, 11.4637, 11.2352, 11.4637],   # 中国平安
    [26.4961, 26.2449, 28.5681, 26.2449, 28.5681],   # 中国人保
    [30.3322, 30.3913, 31.8570, 30.3913, 31.8570],   # 中国人寿
    [15.1806, 15.3320, 16.4334, 15.3320, 16.4334],   # 中国太保
    [18.1243, 18.3291, 19.6948, 18.3291, 19.6948]    # 新华保险
])
row_max = np.max(data,axis=1)
print(row_max)
row_min = np.min(data,axis=1)
print(row_min)
col_max = np.max(data,axis=0)
print(col_max)
col_min = np.min(data,axis=0)
print(col_min)
row_mean = np.mean(data,axis=1)
print(row_mean)
col_mean = np.mean(data,axis=0)
print(col_mean)
all_mean = np.mean(data)
print(all_mean)

row_var = np.var(data,axis=1)
print(row_var)
col_var = np.var(data,axis=0)
print(col_var)
all_var = np.var(data)
print(all_var)
