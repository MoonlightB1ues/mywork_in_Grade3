import numpy as np
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt

future_return = pd.read_excel("../data/期货.xlsx")
print(future_return)
future_return.columns=["date","IF300","IH50","IC500","IM1000",]
future_return["date"]=pd.to_datetime(future_return["date"],format="%Y-%m-%d")

stock_return=pd.read_excel("../data/股票.xlsx")

stock_return.rename(columns={"日期":"date"},inplace=True)
stock_return["date"]=pd.to_datetime(stock_return["date"],format="%Y-%m-%d")
print(stock_return)
stk_portfolio=["date","平安银行","万科A","美的集团","云南白药","泸州老窖","同花顺","中国广核","宁德时代","智飞生物","比亚迪"]
portfolio_return=stock_return.loc[:,stk_portfolio]
portfolio_return.dropna(inplace=True)

for i in stk_portfolio[1:]:
    portfolio_return[f"{i}_return"]=np.log(portfolio_return[f"{i}"])-np.log(portfolio_return[f"{i}"].shift(1))
portfolio_return.dropna(inplace=True)
row_sum =(portfolio_return.iloc[:,11:].sum(axis=1).values)/10

fut_name=["IF300","IH50","IC500","IM1000"]
for i in fut_name:
    future_return[f"{i}_return"]=np.log(future_return[f"{i}"])-np.log(future_return[f"{i}"].shift(1))

future_return.dropna(inplace=True)
for i in fut_name:
    x=future_return[f"{i}_return"].values
    y=row_sum
    b,a=np.polyfit(x,y,1)
    r2=np.corrcoef(x,y)[0,1]**2
    print(r2)

x=future_return["IF300_return"].values
X = sm.add_constant(x)
Y=row_sum
model = sm.OLS(Y, X)
results = model.fit()
# print(results.summary())

print(future_return)
b = results.params[1]
VG = future_return["IF300"].iloc[-1]
N=b*1e8/(VG*300)
print(N)

fig=plt.figure()
ax=fig.add_axes([0.2,0.2,0.7,0.7])
ax.scatter(row_sum,x)
ax.plot(b*x,x)
plt.show()



