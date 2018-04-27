import numpy as np
import scipy as sp
from scipy import constants
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#initial values (all in m and m/s)
scale = 1000                    #1000 ms - 1 to 1
init_x = 10.                    #initial position
init_y = 80.
speed_x = 15./scale             #initial speed
speed_y = 0./scale
accel_x = 0./(scale*scale)      #acceleration
accel_y = -constants.g/(scale*scale)
loss_x = 0.8                    #loss on the border
loss_y = 0.1                    #0 - lossless
    
fig, ax = plt.subplots()

circle, = ax.plot([], [], 'bo', ms=5)
coord = np.array([init_x,init_y])

def init():
    ax.set_xlim([0., 100.])
    ax.set_ylim([0., 100.])
    return circle,

def move():
    global speed_x, speed_y, accel_x, accel_y
    speed_x += accel_x
    speed_y += accel_y
    coord[0] += speed_x
    coord[1] += speed_y
    if coord[0] <= 0. or coord[0] >= 100.:
        speed_x = -((1-loss_x)*speed_x)
        if coord[0] <= 0.:
            coord[0] = 0. - coord[0]    #loss fix
        else:
            coord[0] = 200. - coord[0]  #loss fix
    
    if coord[1] <= 0. or coord[1] >= 100.:	
        speed_y = -((1-loss_y)*speed_y)
        if coord[1] <= 0.:
            coord[1] = 0. - coord[1]    #loss fix
        else:
            coord[1] = 200. - coord[1]  #loss fix
    return(coord[0], coord[1]),
    
def updatefig(frame):
    move()
    circle.set_xdata(coord[0])
    circle.set_ydata(coord[1])
    if (frame%(scale/2)) == 0:
        print((frame/scale)," sec")
    return circle,

anim = animation.FuncAnimation(fig, updatefig, frames=10000, init_func=init, interval=scale/1000, blit=True, repeat=False)

plt.show()