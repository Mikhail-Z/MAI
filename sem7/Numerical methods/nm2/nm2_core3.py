import numpy as np
import matplotlib.pyplot as plt


tay = 0.001
h = 0.001
t = 2
x0 = 0
xl = np.pi
a = 1  # произвольный параметр

alpha=1
beta=-1
gamma=1
theta=-1


def solve(a, b, c, d, n):
    P = np.empty(n)
    Q = np.empty(n)
    P[0] = -c[0]/b[0]
    Q[0] = d[0]/b[0]
    k = n - 1
    for i in range(1, k):
        P[i] = -c[i]/(b[i] + a[i]*P[i-1])
        Q[i] = (d[i] - a[i]*Q[i-1])/(b[i] + a[i]*P[i-1])
    P[k] = 0
    Q[k] = (d[k] - a[k]*Q[k-1])/(b[k]+a[k]*P[k-1])

    x = np.empty(n)
    x[k] = Q[k]
    for i in range(1, n):
        x[k - i] = P[k-i]*x[k - i + 1] + Q[k-i]
    return x

def f(t, x):
    return np.sin(x-a*t) + np.cos(x+a*t)


def term1(x):
    return 0


def term2(x):
    return 0


def term3(x):
    return np.sin(x) + np.cos(x)


def term3_der(x):
    return -(np.sin(x) + np.cos(x))


def term4(x):
    return -a*(np.sin(x) + np.cos(x))


n = 100
m = 10000
h = (xl-x0)/(n-1)
tay = t/(m-1)
X = np.arange(x0, xl+h, h, dtype=np.float_)

u = np.empty([m, n])
x = x0
# ---------------------------трехточечная аппроксимация второго порядка------------------------------------






# ---------------------------явная с первой аппроксимацией по времени-------------------------
'''for i in range(n):
    u[0, i] = term3(x)
    u[1, i] = term3(x) + term4(x)*tay
    x += h

for k in range(1, m-1):
    for j in range(1, n-1):
        u[k+1, j] = a**2*tay**2/h**2*(u[k, j+1] - 2*u[k, j] + u[k, j-1]) + 2*u[k, j] - u[k-1, j]
    x = 0
    u[k+1, 0] = ((u[k-1, 0]-2*u[k, 0])/(2*h*a**2) - 1/h*u[k+1, 1])/((-1/h-1/(h*2*a**2)-1))
    x = h*(n-1)
    u[k+1, n-1] = ((2*u[k, n-1] - u[k-1, n-1])/(2*h*a**2) - (-1/h)*u[k+1, n-2])/(1/h-1+1/(2*h*a**2))

print(a**2*tay**2/h**2)

Y1 = f((m-1)*tay, X)
plt.plot(X, Y1)
plt.plot(X, u[m-1])
plt.show()'''

# -----------------------неявная---------------------------------
'''u = np.empty([m, n])
x = x0
for i in range(n):
    u[0, i] = term3(x)
    u[1, i] = term3(x) + term4(x)*tay
    x += h

a_coef = np.empty(n)
b_coef = np.empty(n)
c_coef = np.empty(n)
d_coef = np.empty(n)

for k in range(1, m-1):
    a_coef[0] = 0
    b_coef[0] = (-1/h-1/(h*2*a**2)-1)
    c_coef[0] = 1/h
    d_coef[0] = (u[k-1, 0]-2*u[k, 0])/(2*h*a**2)
    for i in range(1, n-1):
        a_coef[i] = a**2*tay**2/h**2
        b_coef[i] = -(1+2*a**2*tay**2/h**2)
        c_coef[i] = a**2*tay**2/h**2
        d_coef[i] = -2*u[k, i] + u[k-1, i]
    a_coef[n-1] = (-1/h)
    b_coef[n-1] = 1/h-1+1/(2*h*a**2)
    c_coef[n-1] = 0
    d_coef[n-1] = (2*u[k, n-1] - u[k-1, n-1])/(2*h*a**2)
    Y = solve(a_coef, b_coef, c_coef, d_coef, n)
    u[k+1] = Y

Y1 = f((m-1)*tay, X)
plt.plot(X, Y1)
plt.plot(X, u[m-1])
plt.show()

'''
# ---------------------------явная со второй аппроксимацией по времени-------------------------
'''for i in range(n):
    u[0, i] = term3(x)
    u[1, i] = term3(x) + term4(x)*tay + 0.5*a**2*tay**2*term3_der(x)
    x += h

for k in range(1, m-1):
    for j in range(1, n-1):
        u[k+1, j] = a**2*tay**2/h**2*(u[k, j+1] - 2*u[k, j] + u[k, j-1]) + 2*u[k, j] - u[k-1, j]
    x = 0
    u[k+1, 0] = ((u[k-1, 0]-2*u[k, 0])/(2*h*a**2) - 1/h*u[k+1, 1])/((-1/h-1/(h*2*a**2)-1))
    x = h*(n-1)
    u[k+1, n-1] = ((2*u[k, n-1] - u[k-1, n-1])/(2*h*a**2) - (-1/h)*u[k+1, n-2])/(1/h-1+1/(2*h*a**2))

print(a**2*tay**2/h**2)

Y1 = f((m-1)*tay, X)
plt.plot(X, Y1)
plt.plot(X, u[m-1])
plt.show()
'''
# -----------------------неявная со второй аппроксимацией по времени---------------------------------
u = np.empty([m, n])
x = x0
for i in range(n):
    u[0, i] = term3(x)
    u[1, i] = term3(x) + term4(x)*tay + 0.5*a**2*tay**2*term3_der(x)
    x += h

a_coef = np.empty(n)
b_coef = np.empty(n)
c_coef = np.empty(n)
d_coef = np.empty(n)

for k in range(1, m-1):
    a_coef[0] = 0
    b_coef[0] = (-1/h-1/(h*2*a**2)-1)
    c_coef[0] = 1/h
    d_coef[0] = (u[k-1, 0]-2*u[k, 0])/(2*h*a**2)
    for i in range(1, n-1):
        a_coef[i] = a**2*tay**2/h**2
        b_coef[i] = -(1+2*a**2*tay**2/h**2)
        c_coef[i] = a**2*tay**2/h**2
        d_coef[i] = -2*u[k, i] + u[k-1, i]
    a_coef[n-1] = (-1/h)
    b_coef[n-1] = 1/h-1+1/(2*h*a**2)
    c_coef[n-1] = 0
    d_coef[n-1] = (2*u[k, n-1] - u[k-1, n-1])/(2*h*a**2)
    Y = solve(a_coef, b_coef, c_coef, d_coef, n)
    u[k+1] = Y

Y1 = f((m-1)*tay, X)
plt.plot(X, Y1)
plt.plot(X, u[m-1])
plt.show()


