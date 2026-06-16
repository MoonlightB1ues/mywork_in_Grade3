
import numpy as np
hold_4_19=(5+8+3-4-6)*10000*6.42
print(hold_4_19)
profit=-50000*6.29-80000*6.50+40000*6.47+60000*6.42-30000*6.39+(5+8+3-4-6)*10000*6.42
print(profit)
prices = [6.29, 6.50, 6.47, 6.39, 6.42]
returns = [(prices[i] / prices[i-1] - 1) for i in range(1, len(prices))]
print(returns)
arith_mean = np.mean(returns)
print(arith_mean)
product = np.prod([1.0 + r for r in returns])
geo_mean = product ** (1.0 / len(returns)) - 1
print(geo_mean)
add_hold=700000/611
print(int(add_hold))
hold_4_22=(5+8+3-4-6)*10000*6.11+700000/611
print("交易后资金余额：",hold_4_22)