import numpy as np
default_value = np.array([
    2.5, 3.7, 2.9, 1.8, 0.8, 0.6, 0.6, 0.3, 2.5, 5.0,
    1.2, 0.9, 1.2, 1.2, 0.9, 1.7, 2.1
]) *120e6
print(np.mean(default_value))
# 回收率（% 转换为小数）
recovery_rate = np.array([
    25.2, 21.6, 29.5, 41.4, 58.5, 56.5, 55.0, 55.1, 34.1, 33.8,
    51.5, 45.7, 44.5, 46.1, 47.9, 40.6, 35.0
]) / 100

mu_value=np.mean(default_value)
sigma_value=np.std(default_value)

mu_rate=np.mean(recovery_rate)
sigma_rate=np.std(recovery_rate)

beta=sigma_value**2/mu_value
alpha=mu_value/beta
print("伽马分布的尺度参数和形状参数分别为：",beta,alpha)

gamma_distribution=np.random.gamma(alpha,beta,100000)
print(np.mean(gamma_distribution),np.std(gamma_distribution))

n=mu_rate*(1-mu_rate)/sigma_rate**2-1
alpha_rate=mu_rate*n
beta_rate=(1-mu_rate)*n

beta_distribution=np.random.beta(alpha_rate,beta_rate,100000)
print(np.mean(beta_distribution),np.std(beta_distribution))

