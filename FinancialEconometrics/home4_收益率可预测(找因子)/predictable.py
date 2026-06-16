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

import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

from sklearn import linear_model


#与另外一个程序一样的,看那个即可


data = pd.read_excel('data/1EData_PredictorData2019.xlsx', sheet_name='Monthly')
print(data.shape)

#因子构建
data['DP'] = data['D12'].apply(np.log) - data['Index'].apply(np.log)
data['EP'] = data['E12'].apply(np.log) - data['Index'].apply(np.log)
data['VOL'] = data['CRSP_SPvw'].abs().rolling(window=12).mean()*np.sqrt(pi*6)  #rolling是移动平均,窗口是12个月
data['BILL'] = data['tbl'] - data['tbl'].rolling(window=12).mean()
data['BOND'] = data['lty'] - data['lty'].rolling(window=12).mean()
data['TERM'] = data['lty'] - data['tbl']
data['CREDIT'] = data['AAA'] - data['lty']
data['MA112'] = data['Index'] >= data['Index'].rolling(window=12).mean()
data['MA312'] = data['Index'].rolling(window=3).mean() >= data['Index'].rolling(window=12).mean()
data['MOM6'] = data['Index'] >= data['Index'].shift(periods=6)
data['ExRet'] = data['CRSP_SPvw'] - data['Rfree']
data[['MA112', 'MA312', 'MOM6']] = data[['MA112', 'MA312', 'MOM6']].astype(int)
print(data.iloc[:,:])


factorname=["DP","EP","VOL",'BILL','BOND','TERM','CREDIT','PPIG','IPG','MA112','MA312','MOM6']
fig = plt.figure(figsize=(15, 12))
for i , x in enumerate(factorname):
    ax_sub = fig.add_subplot(4, 4, i + 1)
    # 2. 绘制对应的因子数据，x 就是 "DP", "EP" 等字符串
    ax_sub.plot(data[x])
    # 3. 加上标题，不然分不清谁是谁
    ax_sub.set_title(x,fontsize=12)
plt.tight_layout()
plt.show()


#对数据进行平移

data = pd.concat([data[['yyyymm', 'CRSP_SPvw', 'Rfree', 'ExRet',
                        'DP', 'EP', 'VOL', 'BILL', 'BOND', 'TERM', 'CREDIT', 'PPIG', 'IPG',
                        'MA112', 'MA312', 'MOM6']],
                  data[['DP', 'EP', 'VOL', 'BILL', 'BOND', 'TERM', 'CREDIT', 'PPIG', 'IPG',
                        'MA112', 'MA312', 'MOM6']].shift(periods=1)], axis=1)
data.columns = ['yyyymm', 'Ret', 'Rfree', 'ExRet',
                'DP', 'EP', 'VOL', 'BILL', 'BOND', 'TERM', 'CREDIT', 'PPIG', 'IPG',
                'MA112', 'MA312', 'MOM6', 'DPL1',
                'EPL1', 'VOLL1', 'BILLL1', 'BONDL1', 'TERML1', 'CREDITL1', 'PPIGL1', 'IPGL1',
                'MA112L1', 'MA312L1', 'MOM6L1']
data = data[data['yyyymm'] >= 192701]   #只要1927年之后的数据
data.reset_index(drop=True, inplace=True)
# data[['yyyymm', 'Ret', 'Rfree', 'VOL']].to_csv('data_return_factor.csv', index=False)

data.columns = ['yyyymm', 'Ret', 'Rfree', 'ExRet',
                'DP', 'EP', 'VOL', 'BILL', 'BOND', 'TERM', 'CREDIT', 'PPIG', 'IPG',
                'MA112', 'MA312', 'MOM6',
                'DPL1','EPL1', 'VOLL1', 'BILLL1', 'BONDL1', 'TERML1', 'CREDITL1', 'PPIGL1', 'IPGL1',
                'MA112L1', 'MA312L1', 'MOM6L1']

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

def myfun_econ_gains(rout, rmean, rreal, rfree, volt2, gmm = 5):  #假设市场仅存在两种资产
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

# 样本内检验
# 单因子模型：OLS线性拟合
factor = 'DP'
model = smf.ols('ExRet ~ DPL1', data=data[['ExRet', 'DPL1']])
results = model.fit()
rg_con = results.params['Intercept']
rg_con_pvalue = results.pvalues['Intercept']
rg_DP = results.params['DPL1']
rg_DP_pvalue = results.pvalues['DPL1']
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


# 样本外检验
# 单因子模型: OLS线性拟合
factor_out = 'DP'
num_factor = 1
datafit = data[['yyyymm', 'Ret', 'Rfree', 'ExRet', 'DP', 'DPL1']].copy(deep=True)

n_in = np.sum(datafit['yyyymm'] <= 195612)
n_out = np.sum(datafit['yyyymm'] > 195612)
rout = np.zeros(n_out)
rmean = np.zeros(n_out)
rreal = np.zeros(n_out)
rfree = np.zeros(n_out)
volt2 = np.zeros(n_out)

for i in range(n_out):
    r_fit = datafit['ExRet'].iloc[:(n_in + i)].values
    X_fit = datafit['DPL1'].iloc[:(n_in + i)].values
    X_pred = datafit['DPL1'].iloc[n_in + i]
    if num_factor == 1:
        X_fit = X_fit.reshape(-1, 1)  #把他转成了n*1的向量，-1为占位符
        X_pred = X_pred.reshape(-1, 1)  #把他转成了n*1的向量
    linfits = linear_model.LinearRegression()
    linfits.fit(X_fit, r_fit)
    r_pred = linfits.predict(X_pred)

    #     # model = smf.ols('ExRet ~ DPL1', data=datafit[['ExRet', 'DPL1']].iloc[:(n_in+i),:])
    #     # results = model.fit()
    #     # b = results.params['Intercept']
    #     # k = results.params['DPL1']
    #     # f = datafit['DP'].iloc[n_in+i-1]
    #     # r_pred = k*f+b

    rreal[i] = datafit['ExRet'].iloc[n_in + i]
    rfree[i] = datafit['Rfree'].iloc[n_in + i]
    rout[i] = r_pred
    rmean[i] = np.mean(datafit['ExRet'].iloc[:(n_in + i)].values)
    volt2[i] = np.sum(datafit['Ret'].iloc[(n_in + i - 12):(n_in + i)].values ** 2)

df = pd.DataFrame({'return': rreal,
                   'risk free return': rfree,
                   'predicting return': rout,
                   'historical mean return': rmean,
                   'volatility': volt2})
df.to_csv('data_return.csv', index=False)

print()
print('Out-of-sample tests for one factor model with OLS:')
print('Predictor: {:s}'.format(factor_out))
R2os, MFSEadj, pvalue_MFSEadj = myfun_stat_gains(rout, rmean, rreal)
Uout, Umean, DeltaU = myfun_econ_gains(rout, rmean, rreal, rfree, volt2, gmm=5)



# 样本外检验
# 多因子模型：OLS线性拟合
factor_out = 'DP, EP, VOL, BILL, BOND, TERM, CREDIT, PPIG, IPG, MA112, MA312, MOM6'
datafit = data.copy(deep=True)

n_in = np.sum(datafit['yyyymm'] <= 195612)
n_out = np.sum(datafit['yyyymm'] > 195612)
rout = np.zeros(n_out)
rmean = np.zeros(n_out)
rreal = np.zeros(n_out)
rfree = np.zeros(n_out)
volt2 = np.zeros(n_out)

for i in range(n_out):
    # model = smf.ols('ExRet ~ DPL1 + EPL1 + VOLL1 + BILLL1 + BONDL1 + TERML1 + CREDITL1 + '
    #                 'PPIGL1 + IPGL1 + MA112L1 + MA312L1 + MOM6L1',
    #                 data=datafit[['ExRet', 'DPL1', 'EPL1', 'VOLL1', 'BILLL1', 'BONDL1', 'TERML1',
    #                               'CREDITL1', 'PPIGL1', 'IPGL1', 'MA112L1', 'MA312L1', 'MOM6L1']].iloc[:(n_in+i), :])
    # results = model.fit()
    # k = results.params.values
    # f = datafit[['DP', 'EP', 'VOL', 'BILL', 'BOND', 'TERM', 'CREDIT', 'PPIG',
    #              'IPG', 'MA112', 'MA312', 'MOM6']].iloc[n_in+i-1, :].values
    # f = np.concatenate((np.array([1]), f))
    # r_pred = np.sum(k*f)

    r_fit = datafit['ExRet'].iloc[:n_in + i].values
    X_fit = datafit[
        ['DPL1', 'EPL1', 'VOLL1', 'BILLL1', 'BONDL1', 'TERML1', 'CREDITL1', 'PPIGL1', 'IPGL1', 'MA112L1', 'MA312L1',
         'MOM6L1']].iloc[:(n_in + i), :].values
    X_pred = datafit[
        ['DPL1', 'EPL1', 'VOLL1', 'BILLL1', 'BONDL1', 'TERML1', 'CREDITL1', 'PPIGL1', 'IPGL1', 'MA112L1', 'MA312L1',
         'MOM6L1']].iloc[(n_in + i), :].values.reshape(1, -1)
    linfits = linear_model.LinearRegression()
    linfits.fit(X_fit, r_fit)
    r_pred = linfits.predict(X_pred)

    rreal[i] = datafit['ExRet'].iloc[n_in + i]
    rfree[i] = datafit['Rfree'].iloc[n_in + i]
    rout[i] = r_pred
    rmean[i] = np.mean(datafit['ExRet'].iloc[:(n_in + i)].values)
    volt2[i] = np.sum(datafit['Ret'].iloc[(n_in + i - 12):(n_in + i)].values ** 2)

print()
print('Out-of-sample tests for multi-factor model with OLS:')
print('Predictor: {:s}'.format(factor_out))
R2os, MFSEadj, pvalue_MFSEadj = myfun_stat_gains(rout, rmean, rreal)
Uout, Umean, DeltaU = myfun_econ_gains(rout, rmean, rreal, rfree, volt2, gmm=5)
del datafit

# 样本外检验
# 多因子模型：LASSO回归, Ridge回归，ElasticNet回归

factor_out = 'DP, EP, VOL, BILL, BOND, TERM, CREDIT, PPIG, IPG, MA112, MA312, MOM6'
factor_list = np.array(['DP', 'EP', 'VOL', 'BILL', 'BOND', 'TERM', 'CREDIT', 'PPIG', 'IPG', 'MA112', 'MA312', 'MOM6'])

datafit = data.copy(deep=True)

n_in = np.sum(datafit['yyyymm'] <= 195612)
n_out = np.sum(datafit['yyyymm'] > 195612)
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
    r_fit = datafit['ExRet'].iloc[:(n_in+i)].values
    X_fit = datafit[['DPL1', 'EPL1', 'VOLL1', 'BILLL1', 'BONDL1', 'TERML1', 'CREDITL1', 'PPIGL1', 'IPGL1', 'MA112L1', 'MA312L1', 'MOM6L1']].iloc[:(n_in+i), :].values
    X_pred = datafit[['DPL1', 'EPL1', 'VOLL1', 'BILLL1', 'BONDL1', 'TERML1', 'CREDITL1', 'PPIGL1', 'IPGL1', 'MA112L1', 'MA312L1', 'MOM6L1']].iloc[(n_in+i), :].values.reshape(1, -1)
    # fits = linear_model.Lasso(alpha=0.001, max_iter=10**6, tol=10-6)
    # fits = linear_model.Ridge(alpha=0.001, max_iter=10**6, tol=10-6)
    fits = linear_model.ElasticNet(alpha=0.001, l1_ratio = 0.6, max_iter=10**6, tol=10-6)
    fits.fit(X_fit, r_fit)
    r_pred = fits.predict(X_pred)
    # print(r_pred)

    rreal[i] = datafit['ExRet'].iloc[n_in+i]
    rfree[i] = datafit['Rfree'].iloc[n_in+i]
    rout[i] = r_pred[0]
    rmean[i] = np.mean(datafit['ExRet'].iloc[:(n_in+i)].values)
    volt2[i] = np.sum(datafit['Ret'].iloc[(n_in+i-12):(n_in+i)].values**2)

print('Out-of-sample tests for multi-factor model with ML method:')
print('Predictor: {:s}'.format(factor_out))
R2os, MFSEadj, pvalue_MFSEadj = myfun_stat_gains(rout, rmean, rreal)
Uout, Umean, DeltaU = myfun_econ_gains(rout, rmean, rreal, rfree, volt2, gmm=5)
