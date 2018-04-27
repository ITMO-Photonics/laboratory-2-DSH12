import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

circle, = ax.plot([], [], 'bo', ms=10)
coord = np.array([5.,5.])

def init():
    ax.set_xlim([0., 10.])
    ax.set_ylim([0., 10.])
    return circle,

def updatefig(frame):
    coord[0] += 0.1
    coord[1] += 0.1
    circle.set_xdata(coord[0])
    circle.set_ydata(coord[1])
    return circle,

anim = animation.FuncAnimation(fig, updatefig, frames=5, init_func=init, interval=100, blit=True, repeat=False)

plt.show()
