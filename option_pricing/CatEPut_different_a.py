# compare the results from Monte Carlo Simulation and derived formula

import numpy as np
from numpy import log as ln
from math import exp, sqrt, factorial
from scipy.stats import norm

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter
from matplotlib import cm
import time


@np.vectorize
def cateput_formula(S0, lambd, K, l, A, r, T, sigma):
    k = lambd * (1 - exp(-A))
    price = 0
    # for j in range(l, 20):
    for j in range(l, 10):
        d1 = (ln(S0 / K) - A * j + (k + r) * T) / (sigma * sqrt(T)) + 0.5 * sigma * sqrt(T)
        d2 = d1 - sigma * sqrt(T)
        prob = exp(-lambd * T) * ((lambd * T) ** j) / factorial(j)
        price += (K * exp(-r * T) * norm.cdf(-d2) - S0 * exp(-A * j + k * T) * norm.cdf(-d1)) * prob
    return price


@np.vectorize
def price_diff(price1, price2):
    if not price2:
        return 0
    return (price1 - price2) / price2


if __name__ == "__main__":
    start_time = time.time()
    print(start_time)
    K = 60
    S0 = np.linspace(20, 80, 41)
    lambd = np.linspace(0.1, 2, 20)
    l = 1
    A1 = 0.02
    A2 = 0.2
    r = 0.05
    sigma = 0.2
    T = 1.0
    n = 10000

    xx, yy = np.meshgrid(S0, lambd)
    zz1 = np.array(cateput_formula(xx, yy, K, l, A1, r, T, sigma))
    zz2 = np.array(cateput_formula(xx, yy, K, l, A2, r, T, sigma))
    zz3 = np.array(price_diff(zz2, zz1))

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.plot_surface(xx, yy, zz1, cmap=cm.autumn, linewidth=0, antialiased=False)
    ax.plot_surface(xx, yy, zz2, cmap=cm.winter, linewidth=0, antialiased=False)

    ax.set_title('Lower Surface A = 0.02    Upper Surface A = 0.2')
    ax.xaxis.set_rotate_label(False)  # disable automatic rotation
    ax.yaxis.set_rotate_label(False)  # disable automatic rotation
    ax.zaxis.set_rotate_label(False)  # disable automatic rotation
    ax.set_xlabel('$S_0$', rotation='horizontal')
    ax.set_ylabel('$\lambda$', rotation='horizontal')
    ax.set_zlabel('CatEPut \n Price', rotation='horizontal')
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_locator(MultipleLocator(10))
    ax.set_zlim(0, 40)

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.plot_surface(xx, yy, zz3, cmap=cm.winter, linewidth=0, antialiased=False)

    ax.set_title('Price Difference')
    ax.xaxis.set_rotate_label(False)  # disable automatic rotation
    ax.yaxis.set_rotate_label(False)  # disable automatic rotation
    ax.zaxis.set_rotate_label(False)  # disable automatic rotation
    ax.set_xlabel('$S_0$', rotation='horizontal')
    ax.set_ylabel('$\lambda$', rotation='horizontal')
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_formatter(PercentFormatter(decimals=2))

    plt.show()

    print(time.time() - start_time)
