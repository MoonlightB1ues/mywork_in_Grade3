$由前文推得$
$$
r_{f}=\frac{1}{E[\tilde{m}]}-1
$$
$要得到无风险利率，就是把随机折现因子m表示出来，为了方便，这里定义消费增长率为g，即c_{1}=c_{0}(1+g)$
$$
\tilde{m}=\delta  \frac{u'(c_{0}(1+\tilde{g}))}{u'(c_{0})}
$$
taylor-expand the numerator to second order around $c_{0}$ 
$$
\tilde{m}=\frac{\delta}{u'(c_{0})}\left[ u'(c_{0})+u''(c_{0})c_{0}\tilde{g}+\frac{1}{2}u'''(c_{0})c_{0}^2\tilde{g}^2 \right]
$$
introduce the coefficient of ralative risk aversion and relative prudence
$$
\tilde{m}=\delta\left[ 1-R_{R}\tilde{g}+\frac{1}{2}R_{R}P_{R}\tilde{g}^2 \right]
$$
$$
E[\tilde{m}]=\delta\left( 1-R_{R}\bar{g}+\frac{1}{2}R_{R}P_{R}\bar{g}^2 \right)
$$
we approximate $\bar{g}^2$ by $\sigma_{g}^2$
then we get the $r_{f}$ 
$$
r_{f}=\frac{1-\delta}{\delta}+R_{R}\bar{g}
-\frac{1}{2}R_{R}P_{R}\sigma_{g}^2$$
- 消费者越耐心，就越不需要无风险利率的补偿，利率就越低
- 未来增长越高，因为边际效用递减，消费者就越想要在现在消费，于是需要更高的无风险利率补偿
- 相对风险系数越高,平滑的意愿越强,在未来消费高于现在消费的情况下,更愿意在当前消费更多,因此需要利率补偿.
- 第三项解释为预防性储蓄动机

