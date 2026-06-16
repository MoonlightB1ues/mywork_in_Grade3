import matplotlib.pyplot as plt
import numpy as np
pi=np.pi
plt.rcParams.update({"font.family": "STIXGeneral",
                      "font.size": 20,
                      "mathtext.fontset": "cm"})



x=np.arange(0,10+0.1,0.1)
y_1=np.sin(x)
y_2=np.cos(x)
fig=plt.figure(1)
ax=fig.add_axes([0.2,0.2,0.6,0.7])
ax.plot(x,y_1,'+',label=r'$\sin(x)$')
ax.set_xlabel(r'$x$',fontsize=24)
ax.set_ylabel(r'$\sin(x)$',fontsize=24)

ax2=ax.twinx()
ax2.plot(x,y_2,"*",label=r'$\cos(x)$')
ax2.set_ylabel(r'$\cos(x)$',fontsize=24)

fig.legend(loc='lower right',fontsize=12)
plt.show()
