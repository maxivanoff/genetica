from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from numpy import sin

delta = 2.
s = 3.
a = 2.
v = 3.
X = np.arange(-2, 5, 0.2)
plt.plot(X, a*X*X, '--', color='blue')
plt.plot(X, a*(X-s)**2+delta, '--', color='red')

R = (a*(X-s)**2 + delta - a*X*X)**2 + 4*v*v
Z = (a*(X-s)**2 + delta + a*X*X - np.sqrt(R))*0.5 - 0.5*(a*s*s + delta - np.sqrt((a*s*s + delta)**2 + 4*v*v))

plt.plot(X, Z, '-', color='black')
plt.ylim([0., 5])
plt.show()
plt.close()

