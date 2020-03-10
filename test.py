# estimate pi by simulation

from random import random
count = 0
n = 10000000
for i in range(0, n):
    x = random()
    y = random()
    if x**2 + y**2 <= 1:
        count += 1

print(count / n * 4)