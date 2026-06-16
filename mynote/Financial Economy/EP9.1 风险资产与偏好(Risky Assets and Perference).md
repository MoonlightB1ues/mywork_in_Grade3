$$
\max_{a}E[u(\tilde{w})]=\max_{a}E[u(w_{0}(1+r_{f})+a(\tilde{r}-r_{f}))]
$$
$a表示投资在风险资产的数量,w_{0}为初始财富,要找\bar{a}使得效用最大$
FOC:
$$
E\left(u'[w_{0}(1+r_{f})+a(\tilde{r}-r_{f})]*(\tilde{r}-r_{f})\right)=0
$$
$Prep:$
DARA(decreasing absolute risk aversion)
$$
\bar{a}'(w_{0})>0,当且仅当R'_{A}(w_{0})<0 
$$
$即资产越多,风险厌恶程度降低,且会增加在风险资产上的配置$

$Proof:$
显而易见,证明这个问题需要转换自变量,也就是说,此时把w_0看成自变量
SOC:
$$
E\left ( u''(\tilde{w})(\tilde{r}-r_{f})[(1+r_{f})+\frac{d\tilde{a}}{dw_{0}}(\tilde{r}-r_{f}) ]  \right)
$$
$化简得:$
$$
\frac{d\tilde{a}}{dw_{0}}=-\frac{(1+r_{f})E[u''(\tilde{w})(\tilde{r}-r_{f})]}{E[u''(\tilde{w})(r-r_{f})^2]}
$$
分母中效用函数二阶导小于0,因此只分析分子的符号
$$
E[u''(\tilde{w})(\tilde{r}-r_{f})]=E[-u'(\tilde{w})(\tilde{r}-r_{f})R_{A}(\tilde{w})]
$$
上式和一阶条件做对比,容易看出把$R_{A}(\tilde{w})$放缩出来.这里需要分类讨论
$$
当r_{n}>r_{f}时,w_{n}>w_{0}(1+r_{f}),R_{A}(w_{n})(r_{n}-r_{f})<R_{A}(w_{0}(1+r_{f}))(r_{n}-r_{f})

$$
$$
当r_{n}<r_{f}时,w_{n}<w_{0}(1+r_{f}),仍然有R_{A}(w_{n})(r_{n}-r_{f})<R_{A}(w_{0}(1+r_{f}))(r_{n}-r_{f})
$$
这里是负负得正了,因为$r_{n}-r_{f}$是负的
$$
a'(w_{0})>R_{A}(w_{0}(1+r_{f}))E\left(u'[w_{0}(1+r_{f})+a(\tilde{r}-r_{f})]*(\tilde{r}-r_{f})\right)=0
$$
由此得证.

更进一步,当刻画风险资产投入对初始资产的弹性时,我们认为弹性应该保持为1,对应的相对风险厌恶函数表现为(CRRA)
$$
R'_{R}(w)=0

$$
