import numpy as np
import matplotlib.pyplot as plt


def f(t):
    return 50 + np.exp(t) + np.exp(-t/2) * np.cos(2*np.pi*t) + np.cos(4* t**2)

t1 = np.arange(0.0, 3.0, 0.01)

#subplot(*nrows*, *ncols*, *index*)
# index dice si quieres el grafico en la izqo(1) o en la dcha(2)
plt.figure(figsize= (19,8))
plt.suptitle('Distribucion de graficos')
ax1 = plt.subplot(2, 1, 2)
#usar margins(left,right,both) en vez de x_lims e y_lims
ax1.margins(0.05)           # Default margin is 0.05, value 0 means fit
ax1.plot(t1, f(t1))

ax2 = plt.subplot(221)
ax2.margins(2, 2)           # Values >0.0 zoom out
ax2.set_title('Zoomed out')
ax2.plot(t1, f(t1))

ax3 = plt.subplot(222)
ax3.margins(x=0, y=-0.25)   # Values in (-0.5, 0.0) zooms in to center
ax3.set_title('Zoomed in')
ax3.plot(t1, f(t1))

plt.show()