import numpy as np

# 中国石油
petrochina_close = np.array([7.77, 7.73, 7.69, 7.71, 7.64, 7.76, 7.68, 7.67, 7.67])
petrochina_return = np.array([0.5175, -0.5148, -0.5175, 0.2599, -0.3927,
                               1.5796, -0.6468, -0.1302, 0.0000])
petrochina_return = petrochina_return*0.01

# 中国石化
sinopec_close = np.array([6.03, 5.96, 5.90, 5.83, 5.90, 6.00, 5.88, 5.85, 5.87])
sinopec_return = np.array([1.6863, -1.1609, -1.0067, -1.1864, 1.2007,
                            1.6949, -0.3390, -0.5102, 0.3419])
sinopec_return = sinopec_return*0.01

print("两只股票价格的均值分别为：",np.mean(petrochina_close),np.mean(sinopec_close))
print("两只股票价格的标准差分别为：",np.std(petrochina_close),np.std(sinopec_close))

print("两只股票涨跌幅的均值分别为：",np.mean(petrochina_return),np.mean(sinopec_return))
print("两只股票涨跌幅的标准差分别为：",np.std(petrochina_return),np.std(sinopec_return))

petro_distribution=np.random.normal(np.mean(petrochina_return),np.std(petrochina_return),10000)
print(np.mean(petro_distribution),np.std(petro_distribution))

sinopec_distribution=np.random.normal(np.mean(sinopec_return),np.std(sinopec_return),10000)
print(np.mean(sinopec_distribution),np.std(sinopec_distribution))

mu=np.mean(petrochina_close)
sigma=np.std(petrochina_close)
log_close_expectation=np.log(mu)-(1/2)*np.log(1+(sigma/mu)**2)
log_close_standard=np.log(1+(sigma/mu)**2)**(1/2)

log_distribution=np.random.normal(log_close_expectation,log_close_standard,10000)
print("中国石油价格对数期望与标准差为：",np.mean(log_distribution),np.std(log_distribution))
