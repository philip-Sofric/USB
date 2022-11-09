import math
a = 29
y = 30 - a
health_num = [a]
sick_num = [y]
for i in range(30):
    a = int(a*a/30)
    y = 30 - a
    health_num.append(a)
    sick_num.append(y)
    if y == 30:
        print(f'On {i+1}th day all persons are infected')
        break

print(health_num)
print(sick_num)


