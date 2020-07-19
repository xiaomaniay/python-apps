import math
from scipy.stats import norm
from numpy import log as ln


def calculate_euro_call_price(S, K, D, r, sigma, T, t):
    tao = T - t
    d1, d2 = calculate_d1d2(S, K, D, r, sigma, tao)
    return S * math.exp(-D*tao) * norm.cdf(d1) - K * math.exp(-r*tao) * norm.cdf(d2)


def calculate_euro_put_price(S, K, D, r, sigma, T, t):
    tao = T - t
    d1, d2 = calculate_d1d2(S, K, D, r, sigma, tao)
    return K * math.exp(-r*tao) * norm.cdf(- d2) - S * math.exp(-D*tao) * norm.cdf(- d1)


def calculate_d1d2(S, K, D, r, sigma, tao):
    d1 = (1/(sigma * math.sqrt(tao))) * (ln(S/K) + (r - D + sigma**2/2)*tao)
    d2 = d1 - sigma * math.sqrt(tao)
    return d1, d2


if __name__ == "__main__":
    S = 50
    K = 50
    D = 0.01
    r = 0.03
    sigma = 0.2
    T = 1
    t = 0
    print(calculate_euro_call_price(S, K, D, r, sigma, T, t))
    print(calculate_euro_put_price(S, K, D, r, sigma, T, t))

