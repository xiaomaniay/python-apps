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
def vanilla_formula(S0, K, r, T, sigma):
    d1 = (1 / (sigma * sqrt(T))) * (ln(S0 / K) + (r + sigma ** 2 / 2) * T)
    d2 = d1 - sigma * sqrt(T)
    return  K * norm.cdf(- d2) * exp(-r * T) - S0 * norm.cdf(- d1)


@np.vectorize
def price_diff(price1, price2):
    if not price2:
        return 0
    return (price1 - price2) / price2


if __name__ == "__main__":
    start_time = time.time()
    print(start_time)
    K = 60
    S0 = np.linspace(0, 120, 121)
    lambd = 0.5
    l1 = 1
    l2 = 2
    A = 0.02
    r = 0.05
    sigma = 0.2
    T = 1.0

    yy1 = np.array(cateput_formula(S0, lambd, K, l1, A, r, T, sigma))
    yy2 = np.array(cateput_formula(S0, lambd, K, l2, A, r, T, sigma))
    yy3 = np.array(vanilla_formula(S0, K, r, T, sigma))
    # zz3 = np.array(price_diff(zz2, zz1))

    plt.plot(S0, yy1, label='CatEPut at x = 1')
    plt.plot(S0, yy2, label='CatEPut at x = 2')
    plt.plot(S0, yy3, label='Vanilla Put')
    plt.xlabel('$S_0$')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    print(time.time() - start_time)
