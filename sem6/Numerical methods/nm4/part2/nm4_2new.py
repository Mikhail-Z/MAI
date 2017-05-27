import math
from prettytable import PrettyTable
import numpy as np

def f(x, y, z):
    return (4*y - 4*x*z)/(2*x + 1)

def precise_func(x):
    return 3*x + e**(-2*x)

def p(x):
    #return x
    return 4*x/(2*x+1)

def q(x):
    #return -1
    return 4/(2*x+1)

def g(x):
    return 2*x+1

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




def finite_difference_method(start, finish, h):
    cur_pos = start
    x = []
    y = []
    while cur_pos <= finish:
        y.append(3*cur_pos + math.exp(-2*cur_pos))
        x.append(cur_pos)
        cur_pos += h
    print("y:", y)
    n = len(x)
    first_conditions = [1, 2, -9]
    second_conditions = [1, 0, 1]
    main_matr = np.zeros((n, n))
    gauss = 0
    b = [0]*len(x)
    if first_conditions[0] and first_conditions[1]:
        main_matr[0, 0] = -3/(2*h)*first_conditions[0] + first_conditions[1]
        main_matr[0, 1] = 2/h*first_conditions[0]
        main_matr[0, 2] = -1/(2*h)*first_conditions[0]
        b[0] = first_conditions[2]
        gauss = 1
    elif first_conditions[0] and not first_conditions[1]:
        main_matr[0, 0] = -1/h*first_conditions[0]
        main_matr[0, 1] = 1/h*first_conditions[0]
        b[0] = first_conditions[2]
    if second_conditions[0] and second_conditions[1]:
        main_matr[n-1, n-3] = 1 / (2 * h)*second_conditions[0]
        main_matr[n-1, n-2] = - 2 / h*second_conditions[0]
        main_matr[n-1, n-1] = 3 / (2 * h)*second_conditions[0] + second_conditions[1]
        b[n-1] = second_conditions[2]
        gauss = 1
    elif second_conditions[0] and not second_conditions[1]:
        main_matr[n-1, n-2] = -1/h*second_conditions[0]
        main_matr[n-1, n-1] = 1/h*second_conditions[0]
        b[n-1] = second_conditions[2]
    if gauss:
        for i in range(1, n - 1):
            main_matr[i, i - 1] = 1 - p(x[i]) * h / 2
            main_matr[i, i] = -2 + h ** 2 * q(x[i])
            main_matr[i, i + 1] = 1 + p(x[i]) * h / 2
    print(main_matr, b)
    y = np.linalg.solve(main_matr, b)
    print(y)


def runge_kutt_method(x, step, first_y, first_z):
    y = [first_y]
    z = [first_z]
    delta_y = []
    delta_z = []
    for i in range(len(x)-1):
        K = []
        L = []
        K.append(step*z[i])
        L.append(step*f(x[i], y[i], z[i]))
        for j in range(1, 3):
            K.append(step*(z[i] + 0.5*L[j-1]))
            L.append(step*f(x[i] + 0.5*step, y[i] + 0.5*K[j-1], z[i] + 0.5*L[j-1]))
        K.append(step * (z[i] + L[2]))
        L.append(step * f(x[i] + step, y[i] + K[2], z[i] + L[2]))
        delta_y.append(1/6*(K[0] + 2*K[1] + 2*K[2] + K[3]))
        delta_z.append(1/6*(L[0] + 2*L[1] + 2*L[2] + L[3]))
        y.append(y[len(y)-1] + delta_y[len(delta_y)-1])
        z.append(z[len(z)-1] + delta_z[len(delta_z)-1])
    delta_y.append(None)
    delta_z.append(None)
    return y, z, delta_y, delta_z


if __name__=="__main__":
    start = -2
    finish = 0
    h = 1
    finite_difference_method(start, finish, h)

