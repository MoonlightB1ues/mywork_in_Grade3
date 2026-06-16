### 风险系数
$$
u(y)=\pi u(y+h)+(1-\pi)u(y-h)
$$
$其中\pi为表示达到该效用状态的概率,要解决如何\pi要多大,才弥补遭受的风险$
$$
\begin{aligned}
u(y+h)=u(y)+u'(y)h+\frac{1}{2}u''(y)h^2\\
u(y-h)=u(y)-u'(y)h+\frac{1}{2}u''(y)h^2
\end{aligned}
$$
$代入原式$
$$
u(y)=u(y)+(2\pi-1) u'(y)h+\frac{1}{2}u''(y)h^2
$$
$化简得$
$$
\pi=\frac{1}{2}-\frac{1}{4}\left( \frac{u''(y)}{u'(y)}h \right)
$$
因此定义绝对风险系数$R_{A}(y)$
$$
R_{A}(y)=-\frac{u''(y)}{u'(y)}
$$

如果把h换成$\theta y$可以得到更宽泛的风险厌恶指标
$$
R_{R}(y)=-\frac{yu''(y)}{u'(y)}
$$
	当效用函数确定时,就可以得到具体的风险厌恶系数.但由于推导只限制于局部,因此需要特别的效用函数形式

- 绝对风险厌恶不变型(CARA constant absolute risk aversion)
$$
u(c)=-e^{\alpha c}
$$
$则绝对风险厌恶系数为R_{A}=\alpha$

- 相对风险厌恶不变(CRRA constant relative risk aversion)
$$
u(C)=\frac{c^{1-r}-1}{1-r}
$$
$则相对风险厌恶系数为R_{R}=r,相对审慎系数P_{R}=r+1$
特别的,当r=1时,效用函数退化为
$$
u(c)=\ln c
$$
- 线性效用函数(风险中性)
$$
u(c)=\alpha c
$$
$此时风险厌恶系数都为0$
