# healthy person picking infected

import random
# import matplotlib.pyplot as plt
import numpy as np

num_simulation = 10000
total_persons = 30
person_range = np.arange(1, total_persons + 1, 1)
day_fullyinfected = []
incremental = []
stop_day = 7
for num in range(num_simulation):
    day = 0
    infected_persons = [(random.choice(person_range))]
    num_infection = [len(infected_persons)]
    # print(f'At day {day}, {len(infected_persons)} persons are infected')
    while day < stop_day and num_infection[-1] < 30:
        # count = 0
        infected_today = infected_persons.copy()
        for person in person_range:
            if person not in infected_today:
                # count += 1
                t = random.choice(person_range)
                if t in infected_today:
                    infected_persons.append(person)
        day += 1
        # print(f'At day {day}, {len(infected_persons)} persons are infected')
        num_infection.append(len(infected_persons))
        # print(f'picking persons number is {count}')
    # incremental.append(num_infection[stop_day])

    day_fullyinfected.append(day)
# print(f'new infected {np.average(incremental)} on day {stop_day}')
# print(day_fullyinfected)
print(np.average(day_fullyinfected))
