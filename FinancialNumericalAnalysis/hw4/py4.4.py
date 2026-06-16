import matplotlib.pyplot as plt
import numpy as np
pi=np.pi
plt.rcParams.update({"font.family": "STIXGeneral",
                      "font.size": 20,
                      "mathtext.fontset": "cm"})

t=np.arange(0,2*pi+0.1,0.1)
p_1=np.abs(np.sin(t)*np.cos(t))
p_2=np.abs(np.sin(t)*np.cos(2*t))
p_3=np.abs(np.sin(2*t)*np.cos(t))

fig=plt.figure(1)
ax=fig.add_axes([0.2,0.2,0.7,0.7],projection='polar')
ax.plot(t,p_1)
ax.plot(t,p_2)
ax.plot(t,p_3)

plt.show()