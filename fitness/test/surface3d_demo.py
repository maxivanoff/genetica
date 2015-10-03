from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from numpy import sin

delta = 0.6
s = 8.
a = 0.05
v = 0.7

fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-4, 12, 0.25)
Y = np.arange(-6, 6, 0.25)

X, Y = np.meshgrid(X, Y)
R = (a*(X-s)**2 + delta - a*X*X)**2 + 4*v*v
Z = (a*(X-s)**2 + delta + a*X*X - np.sqrt(R))*0.5 - 0.5*(a*s*s + delta - np.sqrt((a*s*s + delta)**2 + 4*v*v)) + 0.05*Y*Y
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)
#Z = np.exp(-X*X*X/3. + X - Y*Y)
#Z = (sin(R) - 0.5*sin(2*R) + 0.33*sin(3*R) - 0.25*sin(4*R) + 4)*R*R/(R+1)
#Z = X*X*X*X - X*X + Y*Y
#Z = X*X*X + X*X*Y - Y*Y -4*Y
#R = (-2*X + 1 + 1)**2 + 4
#Z = (2*X*X - 2*X + 1 - np.sqrt(R))*0.5
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
ax.set_zlim(0, 3.51)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.xaxis.set_label('X')
ax.yaxis.set_label('Y')

fig.colorbar(surf, shrink=0.5, aspect=5)
#plt.plot(X, Z)
plt.savefig('3d.pdf')
plt.show()

