书上讲的较为笼统,这里只给单因子模型的方法,带来一些直觉

$$
\begin{aligned}
\tilde{r}_{i}=\bar{r}_{i}+\beta_{i}\tilde{f}\\
\tilde{r}_{j}=\bar{r}_{j}+\beta_{j}\tilde{f}\\
\end{aligned}
$$
f在这里理解为风险溢价,或是理解为对不确定性的一种补偿

构造一个资产组合$r_{p}:(w,1-w)$,使得
$$
w_{0}\beta i+(1-w_{0})\beta_{j}=0
$$
此时$r_{p}=r_{f}$,有等式
$$
\frac{\bar{r}_{i}-r_{f}}{\beta_{i}} =\frac{\bar{r}_{j}-r_{f}}{\beta_{j}}=\lambda
$$
再构造一个资产组合$r_{p_{1}}$,使得因子f前的系数为1
$$
r_{p_{1}}=r_{f}+\lambda+\tilde{f}
$$
假设f期望为0,则有
$$
\lambda=\bar{r}_{p_{1}}-r_{f}
$$
代入上上上式有
$$
\bar{r}_{i}=r_{f}+\beta_{i}(\bar{r}_{p_{1}}-r_{f})
$$