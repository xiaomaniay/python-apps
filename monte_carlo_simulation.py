import numpy as np
from math import exp, sqrt
from numpy import log as ln
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MultipleLocator
import numpy as np


def generate_bm(T):
    return sqrt(T) * np.random.normal()


def simulate_stock_price(S, sigma, r, T, W):
    return S * exp((r - 0.5 * sigma**2) * T + sigma * W)


def call_spread_payoff_monte_carlo(S1, S2, sigma1, sigma2, r, T, K, rho, n):
    # simulate sample path n times and calculate the call payoff under each path
    C = []
    discount_factor = exp(-r * T)
    for i in range(0, n):
        # generate two brownian motions with correlation rho
        W1 = generate_bm(T)
        W2 = rho * W1 + sqrt(1 - rho ** 2) * generate_bm(T)

        # Simulate the stock price at option expiry
        S1_T = simulate_stock_price(S1, sigma1, r, T, W1)
        S2_T = simulate_stock_price(S2, sigma2, r, T, W2)

        # Calculate payoff of the call spread
        C.append(max(0.0, S1_T - S2_T - K))

    return discount_factor * (sum(C) / n)


def call_spread_payoff_kirk(S1, S2, sigma1, sigma2, r, T, K, rho):

    discounted_K = K * exp(-r * T)
    y = S2 + discounted_K

    sigma = sqrt(sigma1**2 + (sigma2 * (S2 / y))**2 - 2 * rho * sigma1 * sigma2 * (S2 / y))

    v = sigma * sqrt(T)
    d1 = (ln(S1 / y) + 0.5 * v**2) / v
    d2 = d1 - v

    # Kirk's approximation formula
    return S1 * norm.cdf(d1) - y * norm.cdf(d2)


# fix S1, sigma1, S2, sigma2, rho
def scenario1():
    r = 0.05
    T = 1.0
    n = 500000
    S1 = 30
    sigma1 = 0.1
    S2 = 40
    sigma2 = 0.2
    rho = -0.2
    K = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 20, 25, 30, 35, 40]
    price1 = []
    price2 = []

    for i in range(0, len(K)):
        price1.append(call_spread_payoff_monte_carlo(S1, S2, sigma1, sigma2, r, T, K[i], rho, n))
        price2.append(call_spread_payoff_kirk(S1, S2, sigma1, sigma2, r, T, K[i], rho))

    plt.plot(K, price1)
    plt.plot(K, price2)
    plt.plot(K, [price2[j] - price1[j] for j in range(len(price1))])
    plt.axhline(y=0.0, color='grey', linestyle='--')
    plt.legend(['Monte Carlo Simulation', 'Kirk\'s Approximation', 'Difference'], loc='upper right')
    plt.xlabel("K")
    plt.ylabel("Spread Option")
    plt.axes().yaxis.set_minor_locator(MultipleLocator(0.01))
    plt.show()


# fix S1, sigma1, S2, sigma2, K
def scenario2():
    r = 0.05
    T = 1.0
    n = 500000
    S1 = 30
    sigma1 = 0.1
    S2 = 40
    sigma2 = 0.2
    rho = [-1, -0.9, -0.7, -0.5, -0.2, 0, 0.2, 0.5, 0.7, 0.9, 1]
    K = 5
    price1 = []
    price2 = []

    for i in range(0, len(rho)):
        price1.append(call_spread_payoff_monte_carlo(S1, S2, sigma1, sigma2, r, T, K, rho[i], n))
        price2.append(call_spread_payoff_kirk(S1, S2, sigma1, sigma2, r, T, K, rho[i]))

    plt.plot(rho, price1)
    plt.plot(rho, price2)
    plt.plot(rho, [price2[j] - price1[j] for j in range(len(price1))])
    plt.axhline(y=0.0, color='grey', linestyle='--')
    plt.legend(['Monte Carlo Simulation', 'Kirk\'s Approximation', 'Difference'], loc='upper right')
    plt.xlabel(r'$\rho$')
    plt.ylabel("Spread Option")
    plt.axes().yaxis.set_minor_locator(MultipleLocator(0.01))
    plt.show()


# fix S1, S2, K, rho, sigma2
def scenario3():
    r = 0.05
    T = 1.0
    n = 500000
    S1 = 30
    sigma1 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    S2 = 40
    sigma2 = 0.3
    rho = -0.2
    K = 5
    price1 = []
    price2 = []

    for i in range(0, len(sigma1)):
        price1.append(call_spread_payoff_monte_carlo(S1, S2, sigma1[i], sigma2, r, T, K, rho, n))
        price2.append(call_spread_payoff_kirk(S1, S2, sigma1[i], sigma2, r, T, K, rho))

    plt.plot(sigma1, price1)
    plt.plot(sigma1, price2)
    plt.plot(sigma1, [price2[j] - price1[j] for j in range(len(price1))])
    plt.axhline(y=0.0, color='grey', linestyle='--')
    plt.legend(['Monte Carlo Simulation', 'Kirk\'s Approximation', 'Difference'], loc='upper left')
    plt.xlabel(r'$\sigma_1$')
    plt.ylabel("Spread Option")
    plt.axes().yaxis.set_minor_locator(MultipleLocator(0.1))
    plt.show()


# fix S1, S2, K, rho, sigma1
def scenario4():
    r = 0.05
    T = 1.0
    n = 500000
    S1 = 30
    sigma1 = 0.3
    S2 = 40
    sigma2 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    rho = -0.2
    K = 5
    price1 = []
    price2 = []

    for i in range(0, len(sigma2)):
        price1.append(call_spread_payoff_monte_carlo(S1, S2, sigma1, sigma2[i], r, T, K, rho, n))
        price2.append(call_spread_payoff_kirk(S1, S2, sigma1, sigma2[i], r, T, K, rho))

    plt.plot(sigma2, price1)
    plt.plot(sigma2, price2)
    plt.plot(sigma2, [price2[j] - price1[j] for j in range(len(price1))])
    plt.axhline(y=0.0, color='grey', linestyle='--')
    plt.legend(['Monte Carlo Simulation', 'Kirk\'s Approximation', 'Difference'], loc='upper left')
    plt.xlabel(r'$\sigma_2$')
    plt.ylabel("Spread Option")
    plt.axes().yaxis.set_minor_locator(MultipleLocator(0.1))
    plt.show()



# fix S2, K, rho, sigma1, sigma2
def scenario5():
    r = 0.05
    T = 1.0
    n = 500000
    S1 = [20, 25, 30, 35, 40, 45, 50]
    sigma1 = 0.3
    S2 = 40
    sigma2 = 0.4
    rho = -0.2
    K = 5
    price1 = []
    price2 = []

    for i in range(0, len(S1)):
        price1.append(call_spread_payoff_monte_carlo(S1[i], S2, sigma1, sigma2, r, T, K, rho, n))
        price2.append(call_spread_payoff_kirk(S1[i], S2, sigma1, sigma2, r, T, K, rho))

    plt.plot(S1, price1)
    plt.plot(S1, price2)
    plt.plot(S1, [price2[j] - price1[j] for j in range(len(price1))])
    plt.axhline(y=0.0, color='grey', linestyle='--')
    plt.legend(['Monte Carlo Simulation', 'Kirk\'s Approximation', 'Difference'], loc='upper left')
    plt.xlabel(r'$S_1$')
    plt.ylabel("Spread Option")
    plt.axes().yaxis.set_minor_locator(MultipleLocator(0.1))
    plt.show()


# fix S1, K, rho, sigma1, sigma2
def scenario6():
    r = 0.05
    T = 1.0
    n = 500000
    S1 = 40
    sigma1 = 0.3
    S2 = [20, 25, 30, 35, 40, 45, 50]
    sigma2 = 0.4
    rho = -0.2
    K = 5
    price1 = []
    price2 = []

    for i in range(0, len(S2)):
        price1.append(call_spread_payoff_monte_carlo(S1, S2[i], sigma1, sigma2, r, T, K, rho, n))
        price2.append(call_spread_payoff_kirk(S1, S2[i], sigma1, sigma2, r, T, K, rho))

    plt.plot(S2, price1)
    plt.plot(S2, price2)
    plt.plot(S2, [price2[j] - price1[j] for j in range(len(price1))])
    plt.axhline(y=0.0, color='grey', linestyle='--')
    plt.legend(['Monte Carlo Simulation', 'Kirk\'s Approximation', 'Difference'], loc='upper right')
    plt.xlabel(r'$S_2$')
    plt.ylabel("Spread Option")
    plt.axes().yaxis.set_minor_locator(MultipleLocator(0.1))
    plt.show()


if __name__ == "__main__":

    scenario6()


