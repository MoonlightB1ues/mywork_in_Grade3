
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.family": "STIXGeneral",
                      "font.size": 20,
                      "mathtext.fontset": "cm"})

x=np.arange(0+0.01,50+0.01,0.01)
y_1=x
y_2=np.exp(x)
y_3=np.log10(x)
y_4=np.log(x)
fig=plt.figure(1)
ax_1=fig.add_subplot(2,2,1)
ax_1.set_title(r'$y=x$',fontsize=20)

ax_2=fig.add_subplot(2,2,2)
ax_2.set_title(r'$y=exp(x)$',fontsize=20)
ax_2.set_xticks(ticks=[0,50])
ax_2.set_ylim(0, 60)
ax_2.set_yticks(ticks=[0,20,40],labels=['0','20','40'])

ax_3=fig.add_subplot(2,2,3)
ax_3.set_title(r'$y=lg(x)$',fontsize=20)

ax_4=fig.add_subplot(2,2,4)
ax_4.set_title(r'$y=ln(x)$',fontsize=20)
ax_1.plot(x,y_1)
ax_2.plot(x,y_2)
ax_3.plot(x,y_3)
ax_4.plot(x,y_4)
fig.subplots_adjust(hspace=0.5)

plt.show()