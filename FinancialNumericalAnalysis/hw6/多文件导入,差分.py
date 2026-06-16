
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from envs.my_pythorch.Lib.pydoc import describe
from pandas.core.interchange.dataframe_protocol import DataFrame

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})
import glob

'''data=pd.read_csv("../data/hw6.4data/600000_2007-01-04.txt", sep=",", encoding='GB2312')
data.columns = data.columns.str.strip()
print(data.head())
'''
file_list = glob.glob("../data/hw6.4data/*.txt")  #这个*是一个正则表达式
#print(len(file_list))
database=[pd.read_csv(f, sep=",", encoding='GB2312') for f in file_list]   #将多个数据文件装入这个database,这个database是一个列表,列表中每个元素是一个dataframe
#print(database)
delta_all=[]    #创建一个空矩阵
for df in database:
    df["成交时间"]=pd.to_datetime(df["成交时间"],format='%H:%M:%S')
    #print(df.head())
    #print(df["成交时间"].dtype)

    df["delta"] = df["成交时间"].diff().dt.total_seconds()*(-1)  #找出时间间隔
    df = df[::-1]
    #print(df.head)
    #print(df["delta"].value_counts())
    a=list(df["delta"])
    delta_all.append(a)   #把交易间隔的数据塞到delta_all里面,其中每个列表的元素代表一天的交易间隔数组

delta_all = np.concatenate(delta_all) #将多个数组拼接成一个一维数组
#print(delta_all)
delta_all = delta_all[~np.isnan(delta_all)]  #去掉列表中的Nan
#delta_all = delta_all.astype(int)
values, counts = np.unique(delta_all, return_counts=True)  # 统计不同值的出现情况和频率

#print(values)
#print(counts)


val_feq=pd.DataFrame({"value":values,"count":counts}) #把出现的值和其频率弄成数据库的形式
print(val_feq)

cla=np.logspace(0,4,20)  #class分类,从1到10000分了20个点,时间间隔1-10s出现的频率用一个点来体现
#print(cla)

culm=[]   # 这里的创建方式还很稚嫩,更好的是用culm=np.ones(len(cla))
for i in cla:
    a=0
    for j in range(len(val_feq["value"])):
        if val_feq["value"][j] <= i:
            a+=val_feq["count"][j]
        else:
            break
    culm.append(a)    #得到的是一个累计发生次数
#print(culm)
new_culm=[0]*len(culm)
new_culm[0]=culm[0]
for t in range(1,len(culm)):
   new_culm[t]=culm[t]-culm[t-1]   #得到每个区间的发生次数

n=sum(new_culm)
#print(n)
new_culm[:]=new_culm[:]/sum(new_culm)  #到这里才获得了每个区间的频率分布

new_cla=[0]*len(cla)  #列表创建有n个元素的方式
new_cla[0]=cla[0]
for t in range(1,len(cla)):
   new_cla[t]=cla[t]-cla[t-1]  #也把自变量时间每一个区间的长度取出来

new_cla=np.array(new_cla)  #转成numpy是必要的,列表与列表不能做到相除
new_culm=new_culm[:]/new_cla[:]
cla=cla-new_cla/2  #要把自变量取到区间的中点



def equation(x):
    f=n/x-(1+n/np.sum(np.log(1+delta_all*x)))*np.sum(delta_all/(1+x*delta_all))
    return f

def bisc(a,b,e):
    c = (a + b) / 2
    sign_fc = np.sign(equation(c))
    sign_fa = np.sign(equation(a))
    sign_fb = np.sign(equation(b))
    while b - c > e:
        if sign_fb * sign_fc <= 0:
            a = c
            sign_fa = sign_fc
        else:
            b = c
            sign_fb = sign_fc
        c = (a + b) / 2
        sign_fc = np.sign(equation(c))
    root = c
    return root

xs = np.linspace(0.01, 1, 200)  # theta 图像可视化
ys = [equation(x)/1e4 for x in xs]
plt.figure(figsize=(8,5))
plt.plot(xs, ys)
plt.axhline(0, color='r', linestyle='--')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Checking MLE Equation Sign')
plt.show()

theta=bisc(0.0001,0.1,1e-6)
beta=n/np.sum(np.log(1+delta_all*theta))
print("theta=",theta,"beta=",beta)
q=1/beta+1
mu=theta*beta
print("mu=",mu,"q=",q)

xa=np.linspace(2, 750, 200)
ya=mu*(1+(1-q)*(-1*mu*xa))**(q/(1-q))


fig=plt.figure()
ax=fig.add_axes([0.2,0.2,0.7,0.7])
ax.set_xscale('log',base=10)
ax.set_yscale('log',base=10)
plt.xticks(fontname='Times New Roman', fontsize=30)
plt.yticks(ticks=[1,1e-2,1e-4,1e-6,1e-8],fontname='Times New Roman', fontsize=30)
ax.set_xlabel(r"$τ$",fontsize=36)
ax.set_ylabel(r"$p(τ)$",fontsize=36)
ax.plot(cla,new_culm,'sk',ms=8)
ax.plot(xa,ya,'r',lw=2)
ax.legend(["Emp PDF","Fit q-exp"],fontsize=15,loc='upper right')
plt.show()