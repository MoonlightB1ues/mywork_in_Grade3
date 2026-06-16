import math
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.family": "STIXGeneral",
                      "font.size": 20,
                      "mathtext.fontset": "cm"})

x=np.arange(0+0.01,50+0.01,0.01)
y_2=np.exp(2*x)
fig=plt.figure(1)
ax_2=fig.add_subplot(1,1,1)
ax_2.plot(x,y_2)
plt.show()