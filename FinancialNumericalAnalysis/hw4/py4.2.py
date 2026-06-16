import matplotlib.pyplot as plt
import numpy as np
pi=np.pi
plt.rcParams.update({"font.family": "STIXGeneral",
                      "font.size": 20,
                      "mathtext.fontset": "cm"})



x=np.arange(0+0.01,pi+0.01,0.01)
y=np.sin(x)**x
fig=plt.figure()
ax=fig.add_axes([0.2,0.2,0.7,0.7])
ax.plot(x,y)
ax.set_xlabel(r'$x$',fontsize=24)
ax.set_ylabel(r'$y$',fontsize=24)
ax.set_title(r'$[\sin(x)]^x$',fontsize=24)
plt.show()

