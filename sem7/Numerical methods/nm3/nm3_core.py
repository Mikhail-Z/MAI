import numpy as np


def target_func(x, y):
    return y*np.sin(x)


n = 100
m = 100
x0 = 0
xl = np.pi/2
y0 = 0
yl = 1
h1 = (xl-x0)/(n)
h2 = (yl-y0)/(m)


beta = 1
cur_u = np.zeros((m+1, n+1))

u = np.zeros((m+1, n+1))
u[1:m, 0] = 0
u[1:m, n] = [h2*i for i in range(1, m)]

for i in range(1, m):
    for j in range(1, n):
        u[i, j] = beta

for i in range(1, n):
    u[0, i] = u[1, i] - h2*np.sin(h1*i)
    u[m, i] = u[m-1, i]/(1-h2)

EPS = 0.01


while True:
    for i in range(1, m):
        for j in range(1, n):
            cur_u[i, j] = ((u[i+1, j] + u[i-1, j])/h2**2 + (u[i, j+1] + u[i, j-1])/h1**2 - u[i, j])/\
                          (2/h1**2+2/h2**2)
            for k in range(1, n):
                cur_u[0, k] = u[1, k] - h2 * np.sin(h1 * k)
                cur_u[m, k] = u[m - 1, k] / (1 - h2)

    error = np.max(np.abs(cur_u - u))
    print(error)
    if error < EPS:
        break
    else:
        u = np.copy(cur_u)

for i in range(1, m):
    for j in range(1, n):
        print(target_func(j*h1, i*h2), u[i, j])


'''def create_linear_system(a, b, m, n):
    for j in range(n-1):
        a[j, j] = -1
        a[j, j+n] = 1
        b[j] = h2*np.sin(h1*(j+1))


    for i in range(1, m):
        a[i*(n-1), 0] = 1/h2**2
        for j in range(n-3):'''

