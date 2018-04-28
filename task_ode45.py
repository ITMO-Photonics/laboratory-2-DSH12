from scipy.integrate import ode
from scipy import constants
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

###########################
x0, y0 = 20., 60.           #initial position (m)
t0 = 0.                     #initial time
v0x = 20.                   #initial speed (m/s)
v0y = 20.
accelx = 0.                 #acceleration
accely = -constants.g       #gravitational (Y) acceleration
lossx = 1.                  #1 - lossless
lossy = 1.

def y1(t, y, v0):
    #if y<=0.: 
    #    return 0.
    return (v0+accely*t)

def x1(t, x, v0):
    #if x<=0.:
    #    return 0.
    #if x>=100.:
    #    return 0. 
    return (v0+accelx*t)
###########################
fig, ax = plt.subplots()

circle, = ax.plot([], [], 'bo', ms=8)
coord = np.array([x0,y0])

###########################
#x = ode(x1).set_integrator('vode', method='bdf')
x = ode(x1).set_integrator('dopri5')
x.set_initial_value(x0, t0).set_f_params(v0x)
#y = ode(y1).set_integrator('vode', method='bdf')
y = ode(y1).set_integrator('dopri5')
y.set_initial_value(y0, t0).set_f_params(v0y)

t1 = 30.                    #end time
dt = 0.01                   #dt
frame_count=int(t1//dt)+2   #N of frames for animation
print('t1 = ', t1, ', frame_count = ', frame_count)

resx = x0
resy = y0

reslistx = []
reslisty = []

resindex = 0
rotate_flag=0
last_time = 0.
while y.successful() and resindex <= frame_count+1: 
    if resy < 0. and rotate_flag==0:
        last_time = y.t - last_time
        y.set_initial_value(resy, 0.).set_f_params(lossy*(-y1(last_time,0.,v0y)))
        print('rotate vy = ',(lossy*(-y1(last_time,0.,v0y))), ' time = ', last_time )
        rotate_flag = 1
        v0y=0.-v0y
    resy = y.integrate(y.t+dt)
    reslisty.append(resy)
    if resy > 1.:
            rotate_flag = 0
    resindex += 1
    #height check
    #if resy >= y0-0.0001:
    #    print(y.t+dt, resy, resindex)

resindex = 0
rotate_flag=0
last_time = 0.
while x.successful() and resindex <= frame_count+1:
    if (resx < 0. or resx > 100.) and rotate_flag==0:
        last_time = x.t - last_time
        x.set_initial_value(resx, 0.).set_f_params(lossx*(-x1(last_time,0.,v0x)))
        print('rotate vx = ',(lossx*(-x1(last_time,0.,v0x))), ' time = ', last_time )
        rotate_flag = 1
        v0x=0.-v0x
    resx = x.integrate(x.t+dt)
    reslistx.append(resx)
    if resx > 1. and resx < 99.:
        rotate_flag = 0
    resindex += 1
    #print(x.t+dt, resx, resindex)

def init():
    ax.set_xlim([0., 100.])
    ax.set_ylim([0., 100.])
    return circle,

def updatefig(frame):
    coord[0] = reslistx[frame].real
    coord[1] = reslisty[frame].real
    circle.set_xdata(coord[0])
    circle.set_ydata(coord[1])
    #print(frame)
    return circle,

anim = animation.FuncAnimation(fig, updatefig, frames=frame_count-1, init_func=init, interval=10, blit=True, repeat=False)

plt.show()
