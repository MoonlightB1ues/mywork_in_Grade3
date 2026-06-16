import numpy as np
import pandas as pd
# 设置显示最多 20 列
pd.set_option('display.max_columns', 20)

# 设置显示最多 50 行
pd.set_option('display.max_rows', 50)

# 设置显示宽度，确保 20 列尽量在一行内显示，不换行
pd.set_option('display.width', 1000)
from math import pi
import warnings
warnings.filterwarnings('ignore')
import glob

import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

from sklearn import linear_model

file_list = glob.glob("data/daydata/*.xlsx")
database=[pd.read_excel(f) for f in file_list]
data = pd.concat(database,axis=0,ignore_index=True)  #竖着拼
data.columns=["code","date","close"]
data.dropna(inplace=True)
data["date"] = pd.to_datetime(data["date"],format="%Y-%m-%d")
data["yearmonth"]=data["date"].dt.strftime('%Y%m').astype(int)


data_month=pd.read_csv("data/RESSET_MRESSTK_1.csv")
data_month.columns=["cd","date","close","trdsum","MTTR","rf","pe","eps","roe","ips"]   #trdsum为月成交额,MTTR为月换手率,ips为每股收入
data_beta=pd.read_csv("data/RESSET_SMONRETBETA_BFDT36_1.csv")
data_beta.columns=["cd","date","beta"]
data_month=pd.merge(data_month,data_beta[["date","beta"]],on='date')
data_month['date']=pd.to_datetime(data_month['date'],format='%Y-%m-%d')
data_month['yearmonth'] = data_month['date'].dt.strftime('%Y%m').astype(int)
data_month["r"]=data_month["close"].apply(np.log)-data_month["close"].shift(1).apply(np.log)
data_month.dropna(inplace=True)

#算月波动率
data["r"]=data["close"].apply(np.log)-data["close"].shift(1).apply(np.log)
data.dropna(inplace=True)
vol=data.groupby("yearmonth")["r"].agg(lambda x: (x**2).sum()).reset_index()
vol.rename(columns={"r":"vol"},inplace=True)


#算股价高点
hpoint=data.groupby("yearmonth")["close"].max().reset_index()
hpoint.rename(columns={"close":"hpoint"},inplace=True)


#月已实现偏度
skewness=data.groupby("yearmonth")["close"].agg(lambda x: ((x**3).sum())*len(x)**0.5/((x**2).sum())**1.5).reset_index()
skewness.rename(columns={"close":"skewness"},inplace=True)

data_month=pd.merge(left=data_month,right=vol[["vol","yearmonth"]],on="yearmonth",how="left")
data_month=pd.merge(left=data_month,right=hpoint[["hpoint","yearmonth"]],on="yearmonth",how="left")
data_month=pd.merge(left=data_month,right=skewness[["skewness","yearmonth"]],on="yearmonth",how="left")
data_month["exr"]=data_month["r"]-data_month["rf"]
factorall=["pe","eps","roe","ips","MTTR","beta","vol","hpoint","skewness"]
print(data_month)

data_month = pd.concat([data_month[["date",'yearmonth',"exr","r","rf","pe","eps","roe","ips","MTTR","beta","vol","hpoint","skewness"]],
                  data_month[["pe","eps","roe","ips","MTTR","beta","vol","hpoint","skewness"]].shift(periods=1)], axis=1)
#上期因子用来预测当期数据



data_month.columns = ["date",'yearmonth',"exr","r","rf","pe","eps","roe","ips","MTTR","beta","vol","hpoint","skewness",
                "pel1","epsl1","roel1","ipsl1","MTTRl1","betal1","voll1","hpointl1","skewnessl1"]
data_month.dropna(inplace=True)










# 样本内检验
# 单因子模型：OLS线性拟合
fig = plt.figure(figsize=(15, 12))
fig1 = plt.figure(figsize=(15, 12))
for x,i  in enumerate(factorall):
    factor = i
    model = smf.ols(f'exr ~ {i}l1', data=data_month[['exr', f'{i}l1']])  #指定exr为因变量,factorl1为自变量
    results = model.fit()
    rg_con = results.params['Intercept']   #导出回归结果的统计量
    rg_con_pvalue = results.pvalues['Intercept']
    rg_DP = results.params[f'{i}l1']
    rg_DP_pvalue = results.pvalues[f'{i}l1']
    if rg_DP_pvalue <= 0.01:
        jud = '在1%的显著性水平下有样本内预测能力'
    elif (rg_DP_pvalue > 0.01) & (rg_DP_pvalue <= 0.05):
        jud = '在5%的显著性水平下有样本内预测能力'
    elif (rg_DP_pvalue > 0.05) & (rg_DP_pvalue <= 0.1):
        jud = '在10%的显著性水平下有样本内预测能力'
    else:
        jud = '无样本内预测能力'
    print('In-sample tests for one factor model with OLS:')
    print('Predictor: {:s}'.format(factor))
    print('Regressing Results:  b = {:f},  k = {:f}'.format(rg_con, rg_DP))
    print('Regressing Pvalues: pb = {:f}, pk = {:f}'.format(rg_con_pvalue, rg_DP_pvalue))
    print('Inference: {:s}'.format(jud))
    print("-" * 50)
    ax_sub = fig.add_subplot(4, 4, x + 1)
    ax_sub.plot(data_month[i])    #因子值随时间变化图像
    ax_sub.set_title(i,fontsize=12)
    ax1 = fig1.add_subplot(4, 4, x + 1)
    ax1.scatter(data_month[i],data_month['exr'])  #因子与收益率的相关性
    ax1.set_title(i, fontsize=12)
    ax1.plot(data_month[i],rg_con+rg_DP*data_month[i])  #拟合直线

ax_sub=fig.add_subplot(4, 4, 10)
ax_sub.plot(data_month['exr'])
plt.tight_layout()


plt.show()




#样本外检验
#两个检验函数不必掌握,但要分清rout,rmean,rreal是什么
def myfun_stat_gains(rout, rmean, rreal):    #检验模型是否显著优于基准模型以及历史平均
    R2os = 1 - np.sum((rreal-rout)**2)/np.sum((rreal-rmean)**2)
    d = (rreal - rmean)**2 - ((rreal-rout)**2 - (rmean-rout)**2)
    x = sm.add_constant(np.arange(len(d))+1)
    model = sm.OLS(d, x)
    fitres = model.fit()
    MFSEadj = fitres.tvalues[0]   #MFSE估计量是对因子噪声大于信号的补偿.何为噪声?直观理解为因子x对y真实解释力之外,x和y碰巧产生的相关性.
    pvalue_MFSEadj = fitres.pvalues[0]

    if (R2os > 0) & (pvalue_MFSEadj <= 0.01):
        jud = '在1%的显著性水平下有样本外预测能力'
    elif (R2os > 0) & (pvalue_MFSEadj > 0.01) & (pvalue_MFSEadj <= 0.05):
        jud = '在5%的显著性水平下有样本外预测能力'
    elif (R2os > 0) & (pvalue_MFSEadj > 0.05) & (pvalue_MFSEadj <= 0.1):
        jud = '在10%的显著性水平下有样本外预测能力'
    else:
        jud = '无样本外预测能力'
    print('Stat gains: R2os = {:f}, MFSEadj = {:f}, MFSEpvalue = {:f}'.format(R2os, MFSEadj, pvalue_MFSEadj))
    print('Inference: {:s}'.format(jud))

    return R2os, MFSEadj, pvalue_MFSEadj

def myfun_econ_gains(rout, rmean, rreal, rfree, volt2, gmm = 5):  #假设市场仅存在两种资产,基于效用的经济检验
    omg_out = rout/volt2/gmm
    rp_out = rfree + omg_out*rreal
    Uout = np.mean(rp_out) - 0.5*gmm*np.var(rp_out)
    omg_mean = rmean/volt2/gmm
    rp_mean = rfree + omg_mean*rreal
    Umean = np.mean(rp_mean) - 0.5*gmm*np.var(rp_mean)
    DeltaU = Uout - Umean

    if DeltaU < 10**-6:
        jud = '没有经济意义'
    else:
        jud = '有经济意义'
    print('Econ Gains: Delta U = {:f}, Upred = {:f}, Umean = {:f}'.format(DeltaU, Uout, Umean))
    print('Inference: {:s}'.format(jud))

    return Uout, Umean, DeltaU





# 样本外检验
# 单因子模型: OLS线性拟合
for k in factorall:  #检验各个因子
    factor_out = k
    num_factor = 1
    datafit = data_month[['yearmonth', 'r', 'rf', 'exr', f"{k}" , f"{k}l1" ]].copy(deep=True)
    n_in = np.sum(datafit['yearmonth'] <= 201501)  #划定训练集
    n_out = np.sum(datafit['yearmonth'] > 201501)  #返回大于 201501 的数据行数（即满足该条件的个数）。
    rout = np.zeros(n_out)
    rmean = np.zeros(n_out)
    rreal = np.zeros(n_out)
    rfree = np.zeros(n_out)
    volt2 = np.zeros(n_out)
    for i in range(n_out):
        r_fit = datafit['exr'].iloc[:(n_in + i)].values  #用于拟合的数据,逐次增加
        X_fit = datafit[f"{k}l1"].iloc[:(n_in + i)].values

        X_pred = datafit[f"{k}l1"].iloc[n_in + i]   #根据该期的因子,借助上面拟合的参数,预测下期的结果
        if num_factor == 1:
            X_fit = X_fit.reshape(-1, 1)  #把他转成了n*1的向量，-1为占位符
            X_pred = X_pred.reshape(-1, 1)  #把他转成了n*1的向量
        linfits = linear_model.LinearRegression()
        linfits.fit(X_fit, r_fit)
        r_pred = linfits.predict(X_pred) #r_pred是当期的预测值
        rreal[i] = datafit['exr'].iloc[n_in + i]  #rreal是当期的真实值
        rfree[i] = datafit['rf'].iloc[n_in + i]   #rfree是无风险利率
        rout[i] = r_pred
        rmean[i] = np.mean(datafit['exr'].iloc[:(n_in + i)].values)   #移动历史平均
        volt2[i] = np.sum(datafit['rf'].iloc[(n_in + i - 12):(n_in + i)].values ** 2)  #波动率是为了算经济效用检验
        #跑一次回归然后将历史平均收益，模型预测收益，真实收益存入数组
    df = pd.DataFrame({'return': rreal,
                       'risk free return': rfree,
                       'predicting return': rout,
                       'historical mean return': rmean,
                       'volatility': volt2})
    print()
    print('Out-of-sample tests for one factor model with OLS:')
    print('Predictor: {:s}'.format(factor_out))
    R2os, MFSEadj, pvalue_MFSEadj = myfun_stat_gains(rout, rmean, rreal)
    Uout, Umean, DeltaU = myfun_econ_gains(rout, rmean, rreal, rfree, volt2, gmm=5)
    print("-"*50)


# 样本外检验
# 多因子模型：OLS线性拟合
#思路与单因子模型一致
factor_out = "pe","eps","roe","ips","MTTR","beta","vol","hpoint","skewness"
datafit = data_month.copy(deep=True)

n_in = np.sum(datafit['yearmonth'] <= 201001)
n_out = np.sum(datafit['yearmonth'] > 201001)
rout = np.zeros(n_out)
rmean = np.zeros(n_out)
rreal = np.zeros(n_out)
rfree = np.zeros(n_out)
volt2 = np.zeros(n_out)

for i in range(n_out):
    r_fit = datafit['exr'].iloc[:n_in + i].values
    X_fit = datafit[
        ["pel1","epsl1","roel1","ipsl1","MTTRl1","betal1","voll1","hpointl1","skewnessl1"]].iloc[:(n_in + i), :].values
    X_pred = datafit[
        ["pel1","epsl1","roel1","ipsl1","MTTRl1","betal1","voll1","hpointl1","skewnessl1"]].iloc[(n_in + i), :].values.reshape(1, -1)
    linfits = linear_model.LinearRegression()
    linfits.fit(X_fit, r_fit)
    r_pred = linfits.predict(X_pred)
    rreal[i] = datafit['exr'].iloc[n_in + i]
    rfree[i] = datafit['rf'].iloc[n_in + i]
    rout[i] = r_pred
    rmean[i] = np.mean(datafit['exr'].iloc[:(n_in + i)].values)
    volt2[i] = np.sum(datafit['r'].iloc[(n_in + i - 12):(n_in + i)].values ** 2)

print()
print('Out-of-sample tests for multi-factor model with OLS:')
print(f'Predictor: {factor_out}')
R2os, MFSEadj, pvalue_MFSEadj = myfun_stat_gains(rout, rmean, rreal)
Uout, Umean, DeltaU = myfun_econ_gains(rout, rmean, rreal, rfree, volt2, gmm=5)


# 样本外检验
# 多因子模型：LASSO回归, Ridge回归，ElasticNet回归
#看不懂,只需要把factor_list和datafit定义好就行


factor_list = np.array(["pe","eps","roe","ips","MTTR","beta","vol","hpoint","skewness"])
datafit = data_month.copy(deep=True)
n_in = np.sum(datafit['yearmonth'] <= 201001)
n_out = np.sum(datafit['yearmonth'] > 201001)
rout = np.zeros(n_out)
rmean = np.zeros(n_out)
rreal = np.zeros(n_out)
rfree = np.zeros(n_out)
volt2 = np.zeros(n_out)

# reg = sklm.LassoCV(random_state=0, cv=10, fit_intercept=True, normalize=True, precompute='auto', copy_X=True, n_jobs=-1, max_iter=10**9, tol=10-6)
# reg_lasso = linear_model.LassoLarsCV(cv=10, fit_intercept=True, normalize=True, precompute='auto', copy_X=True, n_jobs=-1, max_iter=10000000)
# reg = sklm.RidgeCV(cv=10, fit_intercept=True)
# reg = sklm.ElasticNetCV(random_state=0, cv=10, fit_intercept=True, normalize=True, precompute='auto', copy_X=True, n_jobs=-1, max_iter=10**9, tol=10-6)
for i in range(n_out):
    r_fit = datafit['exr'].iloc[:(n_in+i)].values
    X_fit = datafit[["pel1","epsl1","roel1","ipsl1","MTTRl1","betal1","voll1","hpointl1","skewnessl1"]].iloc[:(n_in+i), :].values
    X_pred = datafit[["pel1","epsl1","roel1","ipsl1","MTTRl1","betal1","voll1","hpointl1","skewnessl1"]].iloc[(n_in+i), :].values.reshape(1, -1)
    # fits = linear_model.Lasso(alpha=0.001, max_iter=10**6, tol=10-6)
    # fits = linear_model.Ridge(alpha=0.001, max_iter=10**6, tol=10-6)
    fits = linear_model.ElasticNet(alpha=0.001, l1_ratio = 0.6, max_iter=10**6, tol=10-6)
    fits.fit(X_fit, r_fit)
    r_pred = fits.predict(X_pred)
    # print(r_pred)

    rreal[i] = datafit['exr'].iloc[n_in+i]
    rfree[i] = datafit['rf'].iloc[n_in+i]
    rout[i] = r_pred[0]
    rmean[i] = np.mean(datafit['exr'].iloc[:(n_in+i)].values)
    volt2[i] = np.sum(datafit['r'].iloc[(n_in+i-12):(n_in+i)].values**2)

print('Out-of-sample tests for multi-factor model with ML method:')
print(f'Predictor: {factor_out}')
R2os, MFSEadj, pvalue_MFSEadj = myfun_stat_gains(rout, rmean, rreal)
Uout, Umean, DeltaU = myfun_econ_gains(rout, rmean, rreal, rfree, volt2, gmm=5)