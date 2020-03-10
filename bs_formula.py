
import math
from scipy.stats import norm
from numpy import log as ln

# BS formula for call option
S = 100
K = 80
r = 0
sigma = 0.2
T = 1
t = 0
tao = T - t
d1 = (1/(sigma * math.sqrt(tao))) * (ln(S/K) + (r + sigma**2/2)*tao)
d2 = d1 - sigma * math.sqrt(tao)
# c = S * norm.cdf(d1) - K * norm.cdf(d2) * math.exp(-r*tao)
# print(c)


# BS formula for put option
p = K * norm.cdf(- d2) * math.exp(-r*tao) - S * norm.cdf(- d1)
print(p, d1, d2, norm.cdf(- d2))
