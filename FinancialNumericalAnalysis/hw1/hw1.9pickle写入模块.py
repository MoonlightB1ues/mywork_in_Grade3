import pickle
securities = [
    "中信证券", "国泰君安", "海通证券", "华泰证券",
    "广发证券", "招商证券", "申万宏源", "国信证券",
    "中信建投", "中国银河"
]
new_securities = list(enumerate(securities, start=1))
print("列表的个数为：",len(new_securities))
print(new_securities)
profits_2018 = [
    98.7643,  # 中信证券
    70.7004,  # 国泰君安
    57.7071,  # 海通证券
    51.6089,  # 华泰证券
    46.3205,  # 广发证券
    44.4626,  # 招商证券
    42.4781,  # 申万宏源
    34.3125,  # 国信证券
    31.0343,  # 中信建投
    29.3174   # 中国银河
]
total_profits = sum(profits_2018)
mean_profit = total_profits / len(profits_2018)
print("10家公司净利润总额为：",total_profits)
print("10家公司平均利润额为",mean_profit)

returns_q1 = [
    0.547783,  # 中信证券
    0.315274,  # 国泰君安
    0.594318,  # 海通证券
    0.383333,  # 华泰证券
    0.275237,  # 广发证券
    0.307463,  # 招商证券
    0.356265,  # 申万宏源
    0.617682,  # 国信证券
    1.933410,  # 中信建投
    0.734604   # 中国银河
]
closing_prices = [
    27.78,  # 中信证券
    20.15,  # 国泰君安
    14.03,  # 海通证券
    22.41,  # 华泰证券
    16.17,  # 广发证券
    17.52,  # 招商证券
    5.52,   # 申万宏源
    13.54,  # 国信证券
    25.55,  # 中信建投
    11.83   # 中国银河
]
print("最大涨幅为",max(returns_q1))
print("最小涨幅为",min(returns_q1))
closing_prices.sort(reverse=False)
print("从小到大排序为：",closing_prices)
codes = [
    "600030", "601211", "600837", "601688",
    "000776", "600999", "000166", "002736",
    "601066", "601881"
]
datas=list(zip(securities, codes, profits_2018, returns_q1, closing_prices))
print(datas)
output=open("../data.pkl", "wb")
pickle.dump(datas,output,-1)
output.close()
hold_ht=100000/22.45
print("可以买入华泰证券的股数为：",int(hold_ht))