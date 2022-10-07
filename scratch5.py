import numpy as np
import random

RM = np.arange(1, 31, 1)
interation = 1000000

summ = 0
length = []
for i in range(interation):
    sick = [random.choice(RM)]
    sick_today = sick.copy()
    for j in RM:
        if j not in sick_today:
            a = random.choice(RM)
            if a in sick_today:
                sick.append(j)
                summ += 1
    length.append(len(sick))
print('probability of match ', summ / interation)
print('average length is sick is', np.average(length))
