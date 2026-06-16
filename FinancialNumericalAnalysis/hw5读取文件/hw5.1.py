import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})


date=["2019-04-01","2019-04-02",
"2019-04-03",
"2019-04-04",
"2019-04-08",
"2019-04-09",
"2019-04-10",
"2019-04-11",
"2019-04-12",
]
gold_value=pd.Series([1.464,
1.459,
1.466,
1.471,
1.459,
1.454,
1.458,
1.413,
1.406]
, index=date)
date=pd.to_datetime(date,format='%Y-%m-%d')



fund_name=pd.Series([1.466,1.672,1.1770,1.243,1.468]
,index=["国泰金鑫",
"中海医疗",
"华夏优势精选",
"富国城镇发展",
"上投摩根民生"
]
)



medical=np.array([1.657,
1.674,
1.686,
1.638,
1.621,
])

china=np.array([1.1858,
1.1891,
1.1881,
1.1616,
1.1645,
])

construct=np.array([1.240,
1.249,
1.259,
1.233,
1.228
])

date1=[
"2019-04-08",
"2019-04-09",
"2019-04-10",
"2019-04-11",
"2019-04-12"
]
dataframe1=pd.DataFrame(list(zip(medical, china, construct)),columns=["中海医疗保健基金","华夏优势精选股票基金","富国城镇发展股票基金"],index=date1)
print(dataframe1)

medical=np.array([
1.678,
1.664,
1.672,
1.667,
1.657,
1.674,
1.686,
1.638,
1.621
])

china=np.array([1.1599,
1.1564,
1.1770,
1.1884,
1.1858,
1.1891,
1.1881,
1.1616,
1.1645
])

construct=np.array([1.239,
1.239,
1.243,
1.249,
1.240,
1.249,
1.259,
1.233,
1.228

])

morgan=np.array([
1.466,
1.455,
1.468,
1.468,
1.434,
1.431,
1.417,
1.388,
1.385
])

gold=np.array([
1.464,
1.459,
1.466,
1.471,
1.459,
1.454,
1.458,
1.413,
1.406

])
dataframe2=pd.DataFrame([medical, china, construct,gold,morgan],index=["中海医疗保健基金","华夏优势精选股票基金","富国城镇发展股票基金","国泰金鑫","上投摩根民生"],columns=date)
print(dataframe2)


gold_value=gold_value.to_numpy()
print(gold_value)

dataframe1=dataframe1.to_numpy()
print(dataframe1)
