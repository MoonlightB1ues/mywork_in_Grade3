sample1={"date":"2020-8-28","price":6.8654,"margin":-0.0042}
sample2={"date":"2020-8-20","price":8.2048,"margin":-0.0007}
sample3={"date":"2020-8-18","price":8.2048,"margin":-0.0007}
sample4={"date":"2020-8-7","price":9.0959,"margin":-0.0045}
print(sample1.keys())
print(sample2.values())
print(sample3.items())
print(sample1["date"])
print(sample2["price"])
print(sample4["margin"])
sample2["date"]="2020-8-28"
print(sample2)
sample3["前一日中间价"]=0.8940
sample3["前一日涨跌幅"]=-0.0025
print(sample3)
del sample4["margin"]
print(sample4)