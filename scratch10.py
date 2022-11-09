import numpy as np


def fac(num):
    f = 1
    for i in range(num):
        f *= i + 1
    return f


def comb(n, ki):
    return int(fac(n) / (fac(n - ki) * fac(ki)))


# print(comb(5,1))
N = 5825043
# s = 0
# start = int((N - 3) / 2)
# end = int((N + 1) / 2)
# for k in np.arange(start, end + 1, 1):
#     s += comb(N, k)
# pr = pow(1/2, N) * N
# print(pr)
# print(s)
logp = np.log(N*69) - N*np.log(2)
print(logp)