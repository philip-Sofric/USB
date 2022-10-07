import random
import numpy as np

interation = 1000
first_group = np.arange(1, 8, 1)
# first_group = np.arange(8, 31, 1)

total_persons = 30
person_range = np.arange(1, total_persons + 1, 1)
all_sum = 0
for i in range(interation):
    adding = 0
    for j in person_range:
        picking = random.choice(person_range)
        if picking in first_group:
            adding += 1
    all_sum += adding
print('average is ', all_sum/interation)
