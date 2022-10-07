import numpy as np
import random

interation = 1000000
num = np.arange(1, 31, 1)
total_persons = 30
person_range = np.arange(1, total_persons + 1, 1)
accu = 1
for i in num:
    t = i * (total_persons - i) / total_persons
    accu += t
    print(i, accu)
    if accu >= 30:
        break
