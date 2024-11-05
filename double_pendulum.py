### DOUBLE PENDULUM ###

from DEtools_functions import ExRK  # available in my DEtools GitHub repository
from math import sin, cos, pi
from matplotlib import pyplot as plt, animation

# PARAMETERS & EQUATIONS #

inits = [0, [2, 0, 2, 0]]
h = 0.005
n = 4000

m1 = 1; m2 = 1
l1 = 1; l2 = 1
g = 10

def z11(t, zees):
    return zees[1]

def z12(t, zees):
    z11, z12, z21, z22 = zees
    return (-g*(2*m1+m2)*sin(z11)-m2*g*sin(z11-2*z21)
            -2*sin(z11-z21)*m2*(z22**2*l2+z12**2*l1*cos(z11-z21)))/(l1*(2*m1+m2-m2*cos(2*z11-2*z21)))

def z21(t, zees):
    return zees[3]

def z22(t, zees):
    z11, z12, z21, z22 = zees
    return (2*sin(z11-z21)*
        (z12**2*l1*(m1+m2)+g*(m1+m2)*cos(z11)+z22**2*l2*m2*cos(z11-z21)))/(l2*(2*m1+m2-m2*cos(2*z11-2*z21)))

# SOLVE #

data = ExRK(inits, [z11, z12, z21, z22], h, n, 'RK4')

x1 = [l1*sin(data[1][0][i]) for i in range(n+1)]
y1 = [-l1*cos(data[1][0][i]) for i in range(n+1)]

x2 = [x1[i] + l2*sin(data[1][2][i]) for i in range(n+1)]
y2 = [y1[i] - l2*cos(data[1][2][i]) for i in range(n+1)]

# ANIMATE #

fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')

ax.axis('off')

ax.set_xlim(-1.2*(l1+l2), 1.2*(l1+l2))
ax.set_ylim(-1.2*(l1+l2), 1.2*(l1+l2))

ax.text(0, 1.15*(l1+l2), r'$m, l, \theta_0, \omega_0 =$', c='white', size=14, ha='center')
ax.text(0, (l1+l2), f'{m1, m2}, {l1, l2}, {inits[1][0], inits[1][2]}, {inits[1][1], inits[1][3]}', 
                                                                    c='white', size=17, ha='center')

bobs, = ax.plot([], [], marker='o', ms=12, linestyle='None', c='limegreen')
rods, = ax.plot([], [], lw=2.5, c='limegreen')
traj1, = ax.plot([], [], lw=0.5, c='darkgrey')
traj2, = ax.plot([], [], lw=0.5, c='darkgrey')

def update(i):
    bobs.set_data([x1[i], x2[i]], [y1[i], y2[i]])
    rods.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
    traj1.set_data(x1[:i+1], y1[:i+1])
    traj2.set_data(x2[:i+1], y2[:i+1])
    return

anim = animation.FuncAnimation(fig=fig, func=update, frames=n+1, interval=h*1e3)

# SAVE #

anim.save('double_pendulum.mp4')
plt.close(fig)
print('Animation is saved.')