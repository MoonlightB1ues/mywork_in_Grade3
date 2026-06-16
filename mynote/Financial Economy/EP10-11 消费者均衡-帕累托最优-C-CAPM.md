## 消费者均衡
$$
\max_{c_{0},\dots,c_{s} }u(c_{0})+\delta \sum_{s=1}^S \pi_{s}u(c_{s})
$$
$$
\begin{aligned}
s.t. c_{0}+\sum_{s=1}^S \phi_{s}(c_{s}-e_{s}) =e_{0}
\end{aligned}
$$
$其中\phi_{s}为阿罗证券的价格,\pi_{s}是到该状态的概率$
$Lagrange:$
$$
\mathcal{L}=u(c_{0})+\delta \sum_{s=1}^S \pi_{s}u(c_{s})+\lambda \left( e_{0}-c_{0}-\sum_{s=1}^S \phi_{s}(c_{s}-e_{s}) \right)
$$
FOC:
$$

\begin{aligned}
\frac{\partial\mathcal{L}}{\partial c_{0}}=0:&u'(c_{0})=\lambda \\
\frac{\partial\mathcal{L}}{\partial c_{s}}=0:&\delta \pi_{s} u'(c_{s})=\lambda  \phi_{s}
\end{aligned}
$$
结合一阶条件和st看出$\lambda$被$\phi_{s}$和消费c决定.但当后面存在中央调配者时,阿罗证券价格$\phi$变得不再重要,此时消费c决定$\lambda$

## 帕累托最优
	假设存在一个中央调配者,可以任意分配k个人的资源,以使总体资源最大化

$$
\max_{(c_{k 0},c_{k 1},\dots,c_{kS})^K_{k=1}} \sum _{k=1}^K \mu_{k}\left( u_{k}(c_{k0})+\delta  \sum_{s=1}^S \pi_{s}u_{k}(c_{ks})   \right)
$$
$$
\begin{aligned}
s.t. \quad \sum_{k=1}^K c_{k_{0}}& \leq \sum_{k=1}^K e_{k_{0}} \\
            \sum_{k=1}^K c_{k_{s}}& \leq \sum_{k=1}^K e_{k_{s}} \quad s=1,2,\dots,S  
\end{aligned}
$$
$Lagrange'$

$$
\mathcal{L}=\sum _{k=1}^K \mu_{k}\left( u_{k}(c_{k0})+\delta_{k}  \sum_{s=1}^S \pi_{s}u_{k}(c_{ks})   \right)+ \eta_{0}\left( \sum_{k=1}^K e_{k_{0}} - \sum_{k=1}^K c_{k_{0}} \right) + \sum _{s=1}^S \eta_{s} (\sum_{k=1}^K e_{k_{s}}-\sum_{k=1}^K c_{k_{s}})
$$
FOC:
$$
\begin{aligned}
c_{k_{0}}&=u'^{-1}_{k}\left( \frac{\eta_{0}}{\mu_{k}} \right) \\
c_{ks}&=u'^{-1}_{k}\left( \frac{\eta_{s}}{\mu_{k} \delta_{k} \pi_{s}} \right)
\end{aligned}
$$
与消费者均衡一阶条件做对比:
$$
\begin{aligned}
c_{k_{0}}&=u'^{-1}_{k}\left( \lambda_{k} \right) \\
c_{k_{s}}&=u'^{-1}_{k}\left( \frac{\lambda_{k}\phi _{s}}{\delta _{k}\pi _{s}} \right)
\end{aligned}
$$
当$\lambda_{k}=\frac{\eta_{0}}{\mu_{k}}$,$\phi_{s}=\frac{\eta_{s}}{\eta_{0}}$时,消费者跨期均衡与帕累托最优相等.
**由福利经济学第一第二定理,两者等价的条件在理想条件下等价**

## Insight
$另外,此时c_{ks}是\eta_{s}的函数,而当市场出清时,c_{s}=e_{s},因此总禀赋也是\eta的函数,因此,消费者k的消费分布,只与e_{s}(s状态的总禀赋)和u_{k}(其自身财富的现值占总经济的权重)有关,而与消费者在s状态他个人的禀赋无关$
$但也要注意,u_{k}表示消费者k的财富现值,他与e_{ks}是有关的,所以上面的结论没有那么强,但可以有一个较为直观的认识$
$由于消费只与总禀赋有关,因此当禀赋多时,所有消费者都会多消费,即消费者决策正相关$
$每个状态总禀赋的变化可以理解为系统性风险,消费者自身各状态禀赋的变化理解为非系统性风险,一个完善的系统,消费者可以消除自身的非系统性风险,而根据自身的风险厌恶程度,选择承担相应的系统性风险$

## C-CAPM
- 将消费与资产定价联系在一起
- 假设所有消费者的效用函数形式都为HARA
- 为了看清资产的价格,要把消费者均衡中的模型退化一下.(其实这个模型才是原始的,第一个模型是简化推导出的)
$$
\max_{\theta_{0},\dots,\theta_{J} }u(c_{0})+\delta \sum_{s=1}^S \pi_{s}u(c_{s})
$$
$$

\begin{aligned}
s.t. \quad c_{0}&=e_{0}-\sum_{j=1}^Jp_{j}\theta_{j}\\
c_{s}&=e_{s}+\sum_{j=1}^Jx_{s}^j\theta_{j}
\end{aligned}
$$
$这里表示有J种资产,S种状态,其中\theta 表示第J种资产的购买数量,与第一个模型中\theta 表示第S种阿罗证券的数量作区分$

将限制条件代入优化问题,则对$\theta_{j}$的一阶条件有
$$
p_{j}u'(c_{0})=\delta \sum_{s=1}^S\pi _{s}u'(c_{s})x_{s}^j 
$$
$又因为 \frac{x}{p}=1+r$
$$
1=E\left[ \delta   \frac{u'(\tilde{c}_{1})}{u'(c_{0})}(1+\tilde{r}_{j} )  \right]
$$
结合无风险收益率和期望方差公式,可化简为
$$
E(\tilde{r}_{j})-r_{f}=-\frac{\delta(1+r_{f})}{u'(c_{0})}cov[u'(\tilde{c}_{1}),\tilde{r}_{j
}]
$$
$也可更简洁的表达出来$
$$
E(\tilde{r}_{j})-r_{f}=-(1+r_{f})cov(\tilde{m},\tilde{r}_{j})
$$
C-CAPM只需要假设边际效用函数是线性,把随机折现因子$m$替换为r,即可证明,具体过程省略.
- 由上上式看出,雪中送炭的收益率小于锦上添花资产的收益率