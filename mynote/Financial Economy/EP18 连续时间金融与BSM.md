
	随机过程有很强的数学性，数学性的特点是：很多问题是定义上的问题。所以搞清定义对于理解非常重要
### 随机微分
随机微分就是：
$$
dz_{t}
$$
它是一个随机变量，从下式看出
$$
dz_{t}=\lim_{ \Delta \to 0 }(z_{t+\Delta}-z_{t})=\lim_{  \Delta \to 0 } \sum_{i=1}^\Delta \xi_{i}
$$
其中$\xi \sim N(0,1)$,因此$dz_{t} \sim N(0,\Delta)$,也就是说随机微分$dz_{t}$的均值为0，标准差为$\sqrt{ \Delta }$,一段时间往往用dt表示，因此标准差也表示为$\sqrt{ dt }$

### 布朗运动
	后一个时刻的值减去前一个时刻的值服从正态分布是随机过程。
### 广义布朗运动
$$
dx_{t}=udt+\sigma dz_{t}
$$
$x_{t}也是一个随机变量，均值为udt，方差为\sigma^2dt$   

	股票服从布朗运动，那期权服从怎样的过程？期权其实是股票的函数，其实是要研究y=f(x_t）
	于是对y进行泰勒展开。
	微分就是求导,多元微分就是先进行多元泰勒展开,然后把所有的偏导符号都换成微分符号.

### 伊藤引理：
	运用于泰勒展开，要求函数展开到二阶项

$$
\begin{aligned}
dy_{t}&=\frac{\partial f}{\partial x}dx_{t}+\frac{1}{2} \frac{\partial^2 f}{\partial x^2}dx_{t}^2 \\
&将x_{t}拆开化简可得\\
&=\left( \frac{\partial f}{\partial x}u+\frac{1}{2} \frac{\partial^2 f}{\partial x^2} \sigma^2   \right)dt+\frac{\partial f}{\partial x}\sigma dz_{t}
\end{aligned}
$$

### 随机积分
	随机微分给出粒子运动每一时刻位置的变化规律，随机积分则用来给出任意时刻粒子所处位置
定义为：
$$
\int_{t=0}^Tdz_{t}=\lim_{ \Delta \to 0 }[(z_{\Delta}-z_{0})+(z_{2\Delta}-z_{\Delta})+\dots+(z_{T
}-z_{T-\Delta})]=z_{T}-z_{0} \sim N(0,T) 
$$
这里的每一项都可以理解为是步长，1是函数值，仍然沿袭积分的定义，只是最后结果是一个随机变量。

$$

\begin{aligned}
\int_{t=0}^Tdx_{t}&=u\int_{t=0}^Tdt +\sigma\int_{t=0}^Tdz_{t} \\
x_{T}-x_{0}&=uT+\sigma(z_{T}-z_{0})
\end{aligned}
$$
所以$x_{t}$积分的期望为$uT$,方差为$\sigma^2T$

### 几何布朗运动
	由于价格不能为负数,因此考虑把定价移到指数项

$$
S_{t}=e^{ut+\sigma z_{t}}
$$
两边取对数
$$
\ln St=ut+\sigma z_{t}
$$
再两边取微分
$$
\frac{dS_{t}}{St}=udt+\sigma dz_{t}
$$


### BSM定价公式
	从等价鞅和偏微分两个方法来进行理解,与EP17的连续二叉树做对照.
先用随机积分的形式来表示股票的价格
$$
\begin{aligned}
d(\ln S_{t})&=\frac{1}{S_{t}}dS_{t}-\frac{1}{2S_{t}^2}dS_{t}^2 \\
&=udt+\sigma dz_{t}-\frac{1}{2S_{t}^2}(udt+\sigma dz_{t})^2  \\
&=\left( u-\frac{1}{2}\sigma^2 \right)dt+\sigma dz_{t}
\end{aligned}
$$
两边积分有
$$
\begin{aligned}
\ln S_{T}-\ln S_{0}&=\left( u-\frac{1}{2}\sigma^2 \right)T+\sigma \int_{0}^T
dz_{t} \\
S_{T}&=S_{0}e^{\left( u-\frac{1}{2}\sigma^2 \right)T+\sigma \int_{0}^T
dz_{t}}
\end{aligned}
$$
指数项服从均值为$u-\frac{1}{2}\sigma^2$的正态分布,$S_{T}$服从对数正态分布(对数正态分布指的是:随机变量取对数后才服从正态分布),$S_{T}$的均值为:$S_{0}e^{uT}$,又因为在等价鞅测度下,都能满足这个条件$S_{T}=S_{0}e^{rT}$,因此,当我在风险中性世界看S_T的表达式,应该为
$$
S_{T}=S_{0}e^{\left( r-\frac{1}{2}\sigma^2 \right)T+\sigma \int_{0}^T
d\tilde{z_{t}}}
$$
r为无风险利率,$d\tilde{z}$为等价鞅测度下的布朗运动,与原本的dz_t没有计算上的区别(不加证明的说)
接下来就可以写出买入期权的表达式了
$$
C_{0}=max\{S_{T}-K , 0\}
$$
我们现在有的分布是
$$
\ln S_{T} \sim N\left( \ln S_{0}+(u-\frac{1}{2}\sigma^2)T ,\sigma^2T \right)
$$
	![[f7fb82d3ae63cfece8868d4601dcfb33.jpg]]


	偏微分方程的解法困难,因此只把方程推导出来
### BSM方程
	假设市场上存在股票,债券和衍生品,构建股票和衍生品的组合来模拟出债券
构建组合V(t,S_t),其包含一单位衍生品空头,Delta单位的股票东头
$$
V(t,S_{t})=-f(t,S_{t})+\frac{\partial f}{\partial S}S_{t}
$$
![[64b12e93353e61e364076ce80bd4a2af.jpg]]