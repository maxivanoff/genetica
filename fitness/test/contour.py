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

X = np.arange(-4, 12, 0.25)
Y = np.arange(-6, 6, 0.25)

X, Y = np.meshgrid(X, Y)
R = (a*(X-s)**2 + delta - a*X*X)**2 + 4*v*v
Z = (a*(X-s)**2 + delta + a*X*X - np.sqrt(R))*0.5 - 0.5*(a*s*s + delta - np.sqrt((a*s*s + delta)**2 + 4*v*v)) + 0.05*Y*Y

levels = np.array([-0.1, 0.1, 0.25, 0.5, 1.5, 2.5, 4.0, 6.0])
levels = np.arange(-0.1, 4, 0.5)
levels = np.array([-0.1, 0.2, 0.57, 0.85, 1.5, 2.0, 2.5, 3.0, 3.5])
CS = plt.contourf(X, Y, Z, cmap=plt.cm.coolwarm, levels=levels)
CS = plt.contour(X, Y, Z,  colors='black',levels=levels)

#plt.plot(X, Z)
plt.savefig('2d.pdf')
plt.show()

