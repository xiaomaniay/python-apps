# payoff of CatEPut option

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

K = np.array([60] * 21)
S = np.linspace(50, 70, 21)
X = np.linspace(0, 2, 21)
l = 1


@np.vectorize
def payoff(S, X, K, l):
    indicator = 1 if X > l else 0
    return max(K - S, 0) * indicator


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xx, yy = np.meshgrid(S, X)
zz = np.array(payoff(xx, yy, K, l))

ax.plot_surface(xx, yy, zz)

ax.xaxis.set_rotate_label(False)  # disable automatic rotation
ax.yaxis.set_rotate_label(False)  # disable automatic rotation
ax.zaxis.set_rotate_label(False)  # disable automatic rotation
ax.set_xlabel('$S_T$', rotation='horizontal')
ax.set_ylabel('$X_T$', rotation='horizontal')
ax.set_zlabel('Payoff', rotation='horizontal')
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_major_locator(MultipleLocator(0.5))
plt.show()
