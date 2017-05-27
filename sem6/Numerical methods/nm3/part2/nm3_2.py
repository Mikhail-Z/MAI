import numpy as np


def straight_process(a, b, c, free_members):
    size = len(free_members)
    P = [None] * size
    Q = [None] * size

    P[0] = float(-c[0]) / b[0]
    Q[0] = float(free_members[0]) / b[0]
    for i in range(1, size):
        P[i] = -c[i] / (b[i] + a[i] * P[i - 1])
        Q[i] = (free_members[i] - a[i] * Q[i - 1]) / (b[i] + a[i] * P[i - 1])
    return P, Q


def reverse_process(P, Q):
    size = len(P)
    x = [None] * size
    x[size-1] = Q[size-1]
    for i in range(size-2, -1, -1):
        x[i] = P[i]*x[i+1] + Q[i]
    return x


def find_coef(h, y):
    n = len(h)
    a = [0]
    for i in range(1, n-1):
        a.append(h[i])
    b = []
    for i in range(1, n):
        b.append(2*(h[i-1]+h[i]))
    c = []
    for i in range(n-2):
        c.append(h[i+1])
    c.append(0)
    d = []
    for i in range(2, n+1):
        d.append(3*((y[i]-y[i-1])/h[i-1]-(y[i-1]-y[i-2])/h[i-2]))
    return a, b, c, d


def spline_interpolation(x_vals, y_vals):
    h = []
    n = len(x_vals)
    for i in range(1, n):
        h.append(x_vals[i]-x_vals[i-1])

    a_coef, b_coef, c_coef, d_coef = find_coef(h, y_vals)
    print("sweep method. results")
    print("a:", a_coef)
    print("b:", b_coef)
    print("c:", c_coef)
    print("d:", d_coef)
    print("-"*50)
    size = len(d_coef)-1
    for i in range(1, size-1):
        if a_coef[i] == 0 or c_coef[i] == 0:
            print("Error: resistance is not satisfied! (a[i] == 0 or [c[i] == 0)")
    strict_inequality_num = 0
    for i in range(size):
        if abs(b_coef[i]) > abs(a_coef[i]) + abs(b_coef[i]):
            strict_inequality_num += 1
        elif abs(b_coef[i]) < abs(a_coef[i]) + abs(b_coef[i]):
            print("Warning: resistance is not satisfied! (|b[i]| < |a[i]+|c[i]|)")
            break
    if strict_inequality_num == 0:
        print("Warning: resistance is not satisfied! There is no strict inequality at all!")
    P, Q = straight_process(a_coef, b_coef, c_coef, d_coef)

    c = [0]
    c += reverse_process(P, Q)
    a = [y_vals[i] for i in range(n-1)]
    b = [(y_vals[i] - y_vals[i-1])/h[i-1] - 1/3*h[i-1]*(c[i]+2*c[i-1]) for i in range(1, n-1)]
    b += [(y_vals[n-1]-y_vals[n-2])/h[n-2] - 2/3*h[n-2]*c[n-2]]
    d = [(c[i] - c[i-1])/(3*h[i-1]) for i in range(1, n-1)]
    d += [-c[n-2]/(3*h[n-2])]
    print("*"*15)
    print("a:", a)
    print("b:", b)
    print("c:", c)
    print("d:", d)
    i = 0
    print("x vals, ", x_vals)
    while i < n-1 and not(x_vals[i] <= X < x_vals[i+1]):
        i += 1
    if i < n-1:
        print("i:", i)
        return a[i] + b[i]*(X-x_vals[i]) + c[i]*(X-x_vals[i])**2 + d[i]*(X-x_vals[i])**3


if __name__=="__main__":
    X = -0.5
    #x = [-0.4, -0.1, 0.2, 0.5, 0.8]
    #y = [-0.41152, -0.10117, 0.20136, 0.52360, 0.92730]
    x = [-2, -1, 0, 1, 2]
    y = [0.13534,	0.36788,	1.0,	2.7183,	7.3891]
    res = spline_interpolation(x, y)
    print(res)