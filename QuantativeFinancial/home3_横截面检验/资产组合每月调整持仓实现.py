import numpy as np
import pandas as pd

data = pd.read_csv('data/home3/RESSET_MRESSTK_1.csv')
for i in range(2, 9):
    data_read = pd.read_csv('data/home3/RESSET_MRESSTK_' + str(i) + '.csv')
    data = pd.concat((data, data_read), axis=0, ignore_index=True)
    del data_read
print(data.columns)
data.columns = ['stk', 'date', 'close', 'tshare', 'monret', 'monrf', 'pe']    #fshare是总股,tshare是流通股
data.dropna(inplace=True)

print(data)
data['date'] = pd.to_datetime(data['date'])
data['yearmonth'] = data['date'].dt.strftime('%Y%m').astype(int)
data['stksize'] = data['close']*data['tshare']   #流通市值等于流通股乘收盘价
data['stkep'] = 1/data['pe']   #ep是盈利价格比,pe是市盈率
data['monexcret'] = data['monret'] - data['monrf']
data.dropna(inplace = True, subset=['stksize', 'stkep'])


uym = np.unique(data['yearmonth'].values)
print(uym)



class sort_portfolio:   #类的定义方法

    def __init__(self, data, months, gnum):
        self.data = data
        self.months = months
        self.gnum = gnum

    def data_months(self):    #把不同指定月的切片出来,然后横向拼在一起,这里对原数据的要求只是把分组需要的stk,yearmonth,stksize,stkep,monexcret命名好
        dm = self.data.loc[self.data['yearmonth'] == self.months[0], ['stk', 'stksize', 'stkep']]    #分组月的第一个月
        dm.dropna(inplace=True)
        for i in range(1, len(self.months)):
            ind = self.data['yearmonth'] == self.months[i]
            dm = pd.merge(left=dm,
                          right=self.data.loc[ind, ['stk', 'monexcret']],
                          on='stk',
                          how='left',
                          sort=True,
                          suffixes=('', '_' + str(i)))
        dm.columns = ['stk', 'size6', 'ep6', 'ret7', 'ret8', 'ret9', 'ret10', 'ret11',
                      'ret12', 'retn1', 'retn2', 'retn3', 'retn4', 'retn5', 'retn6']
        return dm

    def sort_single_ind(self):   #分组标号
        L = np.sum(self.data['yearmonth'] == self.months[0])    #计算首个月时共有多少股
        n = np.fix(L / self.gnum).astype(int)    #fix是取整,n为分成每组的股票份数
        x = np.ones(L)   #创建一个列表,用于标记每组的标号
        i = 0
        while i < self.gnum:
            if i == self.gnum - 1:
                x[i * n:] = x[i * n:] * i   #给最后一组标号,主要是最后一位需要取到,所以跟前面不一样
            else:
                x[i * n:(i + 1) * n] = x[i * n:(i + 1) * n] * i     #给前四组标号
            i = i + 1
        ssi = x.astype(int)    #取整
        return ssi

    def sort_double_ind(self):  #这是给第二个指标在分好第一组的情况下进行排序
        L = np.sum(self.data['yearmonth'] == self.months[0])
        l = np.fix(L / self.gnum).astype(int)
        n = np.fix(L / (self.gnum ** 2)).astype(int)
        x = np.ones(L)
        i = 0
        while i < self.gnum:
            j = 0
            while j < self.gnum:
                if j == self.gnum - 1:
                    if i == self.gnum - 1:
                        x[(i * l + j * n):] = x[(i * l + j * n):] * j
                    else:
                        x[(i * l + j * n):((i + 1) * l)] = x[(i * l + j * n):((i + 1) * l)] * j
                else:
                    x[(i * l + j * n):(i * l + (j + 1) * n)] = x[(i * l + j * n):(i * l + (j + 1) * n)] * j
                j = j + 1
            i = i + 1
        sdi = x.astype(int)
        return sdi

    def sequence_sort(self):
        dm = self.data_months()
        ssi = self.sort_single_ind()
        sdi = self.sort_double_ind()
        dm.sort_values(by=['size6'], ascending=True, inplace=True)   #先对规模从小到大排序
        dm['sinsort'] = ssi  #再贴上标号
        dm.sort_values(by=['sinsort', 'ep6'], ascending=[True, True], inplace=True) #再在原有标签内,进行ep排序,在已有组别的情况下再贴标签
        dm['dousort'] = sdi
        return dm

    def sequence_sort_mreturn(self):
        sp = self.sequence_sort()
        spmreturn = sp.loc[:, ['ret7', 'sinsort', 'dousort']].dropna().groupby(
            by=['sinsort', 'dousort'])['ret7'].mean()     #返回的是一个25*1的矩阵
        lret = ['ret8', 'ret9', 'ret10', 'ret11', 'ret12', 'retn1', 'retn2', 'retn3', 'retn4', 'retn5', 'retn6']
        for i in lret:
            a = sp.loc[:, [i, 'sinsort', 'dousort']].dropna().groupby(
                by=['sinsort', 'dousort'])[i].mean()
            spmreturn = pd.concat([spmreturn, a], axis=1)
        spmreturn['mret'] = spmreturn.apply(lambda x: x.mean(), axis=1)
        return spmreturn
print(uym.shape)

sp = sort_portfolio(data, uym[5:5+13], 5) #测试第一次
sp.sequence_sort_mreturn()

meanret = []  #进行多年的收益率分组计算
lcname = []
for i in range(5, 230, 12):  #6月是第一个财报披露结束后的月份，234是说我要取到20年数据的最后一个五月
    if len(uym[i:i+13]) == 13:   #这里我改到240,没有改变结果,这是因为加了这个条件,让最后不满12月的数据不计入
        lcname.append(str(uym[i]))
        sp = sort_portfolio(data, uym[i:i+13], 5)
        spmreturn = sp.sequence_sort_mreturn()
        if len(meanret) == 0:
            meanret = spmreturn['mret']
        else:
            meanret = pd.concat([meanret, spmreturn['mret']], axis=1)

meanret.columns = lcname

meanret['meanreturn'] = meanret.apply(lambda x: x.mean(), axis=1) #把多年数据求一个平均

a = meanret['meanreturn'].values.reshape((5,5)) #把25*1的矩阵转换为5*5

print('{:>10s} {:>10s}, {:>10s}, {:>10s}, {:>10s}, {:>10s}'.format('', 'EP1', 'EP2', 'EP3', 'EP4', 'EP5'))
for i in range(5):
    print('{:>10s} {:10.5f}, {:10.5f}, {:10.5f}, {:10.5f}, {:10.5f}'.format('SIZE'+str(i+1),
                                                                            a[i, 0],
                                                                            a[i, 1],
                                                                            a[i, 2],
                                                                            a[i, 3],
                                                                            a[i, 4]))


