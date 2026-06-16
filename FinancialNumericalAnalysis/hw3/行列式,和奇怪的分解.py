import numpy as np
change = np.array([
    [8.2117,  2.2298,  2.3571, 11.3765,  5.2770],   # 杭可科技
    [-4.0458, 0.6972, -2.8895,  3.2742,  5.1003],   # 澜起科技
    [5.7123, 15.9447, -1.8933,  3.7342,  1.7008],   # 心脉医疗
    [3.8217,  0.6732,  1.1043,  1.6990,  2.4105],   # 乐鑫科技
    [12.6468, 2.0497,  3.0867,  4.6562,  4.7228]    # 虹软科技
])
change=1e-2*change
weights = np.array([0.10, 0.15, 0.20, 0.25, 0.30]).reshape(5,1)
wei_price=change.T@weights
print(wei_price)
net_profit=3e7*wei_price
print(net_profit)
accu_profit=np.sum(net_profit)
print("累计盈亏为：",accu_profit)
det_change = np.linalg.det(change) #行列式
print(det_change)
inv_change = np.linalg.inv(change)
eig_change=np.linalg.eig(change)
svd_change=np.linalg.svd(change)

corrcoef_change=np.corrcoef(change)

qr_change=np.linalg.qr(change)
cholesky_change= np.linalg.cholesky(change)