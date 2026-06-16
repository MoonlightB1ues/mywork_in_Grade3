import numpy as np
from numpy.ma.extras import row_stack

data = np.array([
    [3556.66, 3601.67, 3545.10, 3235.08],  # 上证综指
    [4201.12, 4308.79, 4755.93, 4299.14],  # 深证综指
    [1752.39, 1763.23, 1990.95, 1832.08],  # 中小板综指
    [1120.65, 1201.82, 1342.21, 1167.79]   # 创业板综指
])
change_ratio = np.array([
    [1.2311, 1.0127, 0.9843, 0.9126],  # 上证综指
    [1.1408, 1.0256, 1.1038, 0.9040],  # 深证综指
    [1.1141, 1.0062, 1.1291, 0.9202],  # 中小板综指
    [1.1431, 1.0724, 1.1168, 0.8700]   # 创业板综指
])

row_sum = np.sum(data,axis=1)
print(row_sum)
col_sum = np.sum(data,axis=0)
print(col_sum)
all_sum = np.sum(data)
print(all_sum)

ln_data = np.log(data)

exp_data = np.exp(ln_data)
print(exp_data)

ratio_row_sum = np.sum(change_ratio,axis=1)
print(ratio_row_sum)
