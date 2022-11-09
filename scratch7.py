import matplotlib.pyplot as plt
import random
import numpy as np

simulation_num = 500
total_person = 30
day_to_max = []
for i in range(simulation_num):
    day = 0
    infected_array = [random.choice(range(total_person))]
    infected_num_by_day = [len(infected_array)]
    while infected_num_by_day[-1] < total_person:
        infected_today = infected_array.copy()
        infected_new = []
        for person in range(total_person):
            if person in infected_today:
                random_pick = random.choice(range(total_person))
                if (random_pick not in infected_today) and (random_pick not in infected_new):
                    infected_array.append(random_pick)
                    infected_new.append(random_pick)
        infected_num_by_day.append(len(infected_array))
        day += 1
    print(infected_num_by_day)
    day_to_max.append(day)
    # print('Day to all infected is ', day)
    # plt.plot(range(day+1), infected_num_by_day, label=f's{i+1},max_day{day_to_max[-1]}')
    # plt.xlabel('day')
    # plt.ylabel('Infected persons')
    # plt.title('Infection speed')
    # plt.legend()

print('Average fully infected days are', np.average(day_to_max))
# plt.show()
