import numpy as np
import pandas as pd

# 设置显示最多 20 列
pd.set_option('display.max_columns', 20)
# 设置显示最多 50 行
pd.set_option('display.max_rows', 50)
# 设置显示宽度，确保 20 列尽量在一行内显示，不换行
pd.set_option('display.width', 1000)
np.set_printoptions(
    linewidth=1000,    # 每行最多显示多少个字符，防止折行
    threshold=1000,    # 数组元素总数超过这个值时，中间部分会显示为省略号 ...
    precision=4,       # 小数点后保留几位
    suppress=True      # 禁用科学计数法，强制显示小数
)
from math import pi
import warnings
warnings.filterwarnings('ignore')
import glob
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from sklearn import linear_model


data=pd.read_csv("RESSET_IDXMONRET_1.csv")   #导入各板块指数数据
data.columns=["number","cd","index","date","r"]
index=data["index"].unique()


data["date"]=pd.to_datetime(data["date"],format="%Y-%m-%d")
data['yearmonth'] = data['date'].dt.strftime('%Y%m').astype(int)
data.drop(["number","cd"],axis=1,inplace=True)


# 1. 直接透视：以日期为行，以 index 的不同值为列名，把 r 的值填进去
new_data = data.pivot(index='yearmonth', columns='index', values='r')
# 2. 此时 'date' 变成了行索引(Index)，reset使得行索引变为普通的列
new_data = new_data.reset_index()
# 3. （可选）透视后，表头(columns)会带有一个名字叫 'index'，清空它让表格看起来更干净
new_data.columns.name = None
print(new_data)

factor_data=pd.read_csv("RESSET_THRFACDAT_MONTHLY_1.csv") #导入三因子各期数据
factor_data.drop(["Exchflg","Mktflg"],axis=1,inplace=True)
factor_data.columns=["date","rmrf","smb","hml"]
factor_data["date"]=pd.to_datetime(factor_data["date"],format="%Y-%m-%d")
factor_data['yearmonth'] = factor_data['date'].dt.strftime('%Y%m').astype(int)


new_data=pd.merge(factor_data,new_data,on=['yearmonth'],how='left')
print(new_data)

rf_data=pd.read_csv("RESSET_MRESSTK_1.csv")  #导入无风险收益率

rf_data.columns=["date","rf"]
rf_data["date"]=pd.to_datetime(rf_data["date"],format="%Y-%m-%d")
rf_data['yearmonth'] = rf_data['date'].dt.strftime('%Y%m').astype(int)
new_data=pd.merge(new_data,rf_data,on=['yearmonth'],how='left')


# index=[c for c in new_data.columns if c.startswith('上证')]

old_data=new_data.copy()
time_points = sorted(old_data[old_data["yearmonth"] >= 201801]["yearmonth"].unique())  #从2018年开始取，只取yearmonth，取完unique去重，从小到大排序
time_series =old_data[old_data["date_x"] >="2018-01-01"]["date_x"]  #再取一次日期是因为这是时间格式，方便画图


#清洗数据后开始估计协方差阵，这什么石山代码我靠？？？
w_series=[]
w_star_series=[]
mean_series=[]
mean_star_series=[]
sigma_series=[]
sigma_star_series=[]
sharpe_series=[]
sharpe_star_series=[]
for tennor in time_points:   #循环是为了每月都算一个协方差阵
    def CovarianceMatrix_history(tennor):
        global index
        data=old_data[old_data["yearmonth"]<=tennor]   #划出样本集而不污染原始样本
        #协方差阵
        R = data[index].sub(data['rf'], axis=0).values   #将各指数收益率减去无风险资产，最后返回的是np，形状为（T，N）
        Cov_Sample1 = np.cov(R, rowvar=False)   #每一列是一个变量,每一行是一个观测点
        return Cov_Sample1,R,data
    Cov_Sample1, R,new_data = CovarianceMatrix_history(tennor)

    # 因子模型的beta估计    Y为T*N,X为T*K+1,b为K+1 * N(N个资产,每个资产有K+1个参数),多维线性回归做的对不对看维度就行
    def CovarianceMatrix_factor(new_data,R):
        X = np.concatenate([np.ones((len(new_data["rmrf"]), 1)), new_data[["rmrf","smb","hml"]]], axis=1) #这是在拼右边的X
        Y= R
        AB_hat = np.linalg.inv(X.T@X)@(X.T@Y)  #AB_hat即估计出来的b
        ALPHA = AB_hat[0]    #第0行是阿尔法
        BETA = AB_hat[1:4]     #第一到三行是贝塔
        RESD = Y - X@AB_hat  #RESD仍为T*N
        #因子模型协方差阵  因子协方差阵的二次型加误差的协方差阵
        X_factor=BETA.T@np.cov(new_data[["rmrf","smb","hml"]].values, rowvar=False)@BETA   #这里有一个是否去均值的问题,首先cov自动去了,其次,容易证对因子f去均值等同于对R去均值(因为阿尔法和贝塔是常数,贝塔各期不变)
        epsilon_full=np.cov(RESD, rowvar=False)
        epsilon_diag = np.diag(np.diag(epsilon_full))  #np.diag为先提出对角元,对提出的对角元扩展为矩阵
        Cov_Sample2=X_factor+epsilon_diag
        #print(f"{tennor}时,因子模型协方差为:",Cov_Sample2)
        return Cov_Sample2
    Cov_Sample2 = CovarianceMatrix_factor(new_data,R)

    def CovarianceMatrix_Shrink(Cov_Sample1,R):
        #压缩模型,这里跟教材不一样,是因为文献原因
        # 假设 Cov_Sample1 是之前算的 10x10 协方差阵
        Sigma = Cov_Sample1
        n = Sigma.shape[0]        # 资产个数 (10)
        T = R.shape[0]            # 时间长度 (样本行数)
        Id_n = np.eye(n)          # n维单位矩阵
        # 计算 tr(Sigma) 和 tr(Sigma^2)
        tr_Sigma = np.trace(Sigma)
        tr_Sigma_sq = np.trace(Sigma @ Sigma) # 注意是矩阵乘法后的迹
        # --- 计算分子 (Numerator) ---
        num = (1 - 2/n) * tr_Sigma_sq + (tr_Sigma)**2
        # --- 计算分母 (Denominator) ---
        den = (T - 2/n) * (tr_Sigma_sq - (tr_Sigma**2 / n))
        # 计算 rho，限制在 [0, 1] 之间
        rho = min(num / den, 1.0)
        #print(f"最优收缩强度 rho: {rho:.4f}")
        # 第一项: (1 - rho) * Sigma
        part1 = (1 - rho) * Sigma
        # 第二项: rho * (tr(Sigma) / n) * Id_n
        part2 = rho * (tr_Sigma / n) * Id_n
        # 最终矩阵
        Cov_sample5 = part1 + part2
        #print(f"{tennor}时,压缩模型协方差为:" , Cov_sample5)
        return Cov_sample5
    Cov_sample5 = CovarianceMatrix_Shrink(Cov_Sample1,R)


    #风险最小化估计权重,如果指定了收益率,需要对l和b相应修改,构造A和b,方差阵自己指定
    #最小化期望风险,不指定期望收益率
    l=np.ones(10).reshape(1,-1) #-1为根据维度自动调整,(1,10)
    b=1
    sigma=Cov_Sample2
    sigma_i=np.linalg.inv(sigma)
    w=sigma_i@l.T@np.linalg.inv(l@sigma_i@l.T)
    w_series.append(w)

    #最大化期望效用
    gamma=3
    rex = np.mean(R, axis=0)  # 每个资产的平均收益,返回的是(N,)
    Q=gamma*Cov_sample5
    c=-1*rex  #注意这里有坑,c不是一个向量,没有纵轴
    A=l  #这里的A是竖着的
    N = Q.shape[0]
    # 1. 确保所有输入都是严格的二维列向量 (N, 1) 或 (K, 1)
    # 这一步是防止出现 (N,) 这种一维数组导致计算混乱的关键
    c_vec = c.reshape(N, 1)
    Q_inv = np.linalg.inv(Q)
    # 中间核心项 M = (A @ Q^-1 @ A.T)^-1
    M = np.linalg.inv(A @ Q_inv @ A.T)
    term1 = Q_inv @ A.T @ M
    P = np.eye(N) - (A.T @ M @ A @ Q_inv)
    # 最终 term2 维度: (N,N) @ (N,N) @ (N,1) = (N, 1)
    term2 = Q_inv @ P @ c_vec
    # 4. 合并结果
    w_star = term1 - term2 #得到最大效用估计的权重
    w_star_series.append(w_star)


    #权重都算出来了,现在算组合的均值和方差
    mean_portfolio = np.dot(w.T, rex)   #最小方差组合的收益
    mean_series.append(mean_portfolio)

    mean_portfolio_star=np.dot(w_star.T, rex)  #最大效用的收益
    mean_star_series.append(mean_portfolio_star)

    sigma_portfolio = w.T@Cov_Sample2@w  #最小方差组合的方差
    sigma_series.append(sigma_portfolio)

    sigma_portfolio_star = w_star.T @ Cov_sample5 @ w_star
    sigma_star_series.append(sigma_portfolio_star)

    sharpe=mean_portfolio/sigma_portfolio #最小方差的夏普比
    sharpe_series.append(sharpe)

    sharpe_star=mean_portfolio_star/sigma_portfolio_star
    sharpe_star_series.append(sharpe_star)


# 将列表转换为 DataFrame
# w.ravel() 会把 (10, 1) 的向量变成 (10,) 的一维数组
df_w = pd.DataFrame(
    [w.ravel() for w in w_series],
    index=time_series,
    columns=index
)

df_w_star = pd.DataFrame(
    [w.ravel() for w in w_star_series],
    index=time_series,
    columns=index
)


# 绘制最小风险组合权重
df_w.plot(figsize=(12, 6), title="Minimum Variance Portfolio Weights Over Time")
plt.legend( loc='lower left',labels=["xinxi","gongyong","yiyao","kexuan","gongye","cailiao","xiaofei","nengyuan","tongxin","jinrong"])
plt.xlabel("Time")
plt.ylabel("Weight")
plt.show()

# 绘制最大效用组合权重
df_w_star.plot(figsize=(12, 6), title="Max Utility Portfolio Weights Over Time")
plt.xlabel("Time")
plt.ylabel("Weight")
plt.legend( loc='lower left',labels=["xinxi","gongyong","yiyao","kexuan","gongye","cailiao","xiaofei","nengyuan","tongxin","jinrong"])
plt.show()
print("风险最小投资组合的收益均值为",np.mean(mean_portfolio),"风险最小组合的标准差均值为",np.mean(sigma_portfolio),"夏普比均值为:",np.mean(sharpe_series))
print("效用最大投资组合的收益均值为",np.mean(mean_portfolio_star),"效用最大组合的标准差均值为",np.mean(sigma_portfolio_star),"夏普比均值为:",np.mean(sharpe_star_series))


# 为保证代码运行效率,所以没把这两个方差阵的估计加入循环
# #常数协方差阵
# # 1. 提取对角线（方差），计算其平均值
# avg_var = np.diag(Cov_Sample1).mean()
# # 2. 计算非对角线的平均协方差
# # 先求所有元素的和，减去对角线元素之和，再除以非对角线元素的个数
# n = Cov_Sample1.shape[0]
# total_sum = Cov_Sample1.sum()
# diag_sum = np.diag(Cov_Sample1).sum()
# avg_cov = (total_sum - diag_sum) / (n * (n - 1))
# # 3. 创建一个全为 avg_cov 的矩阵
# New_Cov = np.full((n, n), avg_cov)
# # 4. 将对角线替换为 avg_var
# # np.fill_diagonal 会直接修改原对象
# np.fill_diagonal(New_Cov, avg_var)
# Cov_sample3=New_Cov
# print(f"{tennor}时,常数协方差为:",Cov_sample3)
#
#
# #指数加权移动平均阵
# lam=0.95
# EWMA=np.cov(R[0:-1,:], rowvar=False)
# R_mean = np.mean(R[:,:], axis=0)
# err = R[-1, :] - R_mean
# Cov_sample4 = lam * EWMA + (1 - lam) * np.outer(err, err)  #outer为外积
# print(f"{tennor}时,指数加权移动平均协方差为:" , Cov_sample4)
