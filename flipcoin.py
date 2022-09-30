from random import random
import matplotlib.pyplot as plt

import numpy as np


def throwcoins(n):
    event = []
    for i in range(n):
        throw = random()
        if throw >= 0.5:
            event.append(1)
        else:
            event.append(0)
    return event


def findHHHH(arr):
    length = len(arr)
    count = 0
    if length < 4:
        return -1
    else:
        for i in range(length):
            if i >= length - 3:
                break
            elif arr[i] == 1 and arr[i+1] == 1 and arr[i+2] == 1 and arr[i+3] == 1:
                count += 1
            else:
                continue
    return count


# ae = throwcoins(20)
# print('array is ', ae)
# print('number of HHHH is ', findHHHH(ae))
K = []
for j in range(3000):
    result_array = throwcoins(100)
    K.append(findHHHH(result_array))
x = sum(K)
K = np.array(K)
plt.hist(K)
plt.show()