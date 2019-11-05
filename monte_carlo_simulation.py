import numpy as np
from scipy.stats import norm
import math

S0 = 100
K = 110
sigma = 0.3
r = 0.05
T = 0.5

# Black-Scholes_Merton formula
d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T)/(sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)
N1 = norm.cdf(d1)
