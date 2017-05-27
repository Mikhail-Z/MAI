import math
from prettytable import PrettyTable
import numpy as np
import matplotlib.pyplot as plt


def f(x, y, z):
    return (4*y - 4*x*z)/(2*x+1)


def precise_y(x):
    return 3*x + math.exp(-2*x)

def p(x):
    return 4*x

def q(x):
    return -4

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
    while round(cur_pos, 6) <= finish:
        y.append(3*cur_pos + math.exp(-2*cur_pos))
        x.append(cur_pos)
        cur_pos += h
    n = len(x)
    first_conditions = [0.5, 1, 4.5]
    second_conditions = [1, 0, 3 - 2 * math.exp(-4)]
    if first_conditions[0] != 0:
        a = [None] * n
        b = [None] * n
        c = [None] * n
        d = [0] * n
        a[0] = 0
        b[0] = -first_conditions[0]/h+first_conditions[1]
        c[0] = first_conditions[0]/h
        d[0] = first_conditions[2]
        s = 1
        for i in range(s, n - 1):
            a[i] = 1*g(x[i]) - p(x[i]) * h / 2
            b[i] = -2*g(x[i]) + (h ** 2) * q(x[i])
            c[i] = 1*g(x[i]) + p(x[i]) * h / 2
        if second_conditions[0] != 0:
            a[n-1] = -second_conditions[0] / h
            b[n-1] = second_conditions[0] / h + second_conditions[1]
            c[n-1] = 0
            d[n-1] = second_conditions[2]
        else:
            a[n-1] = 1*g(x[n-1])-p(x[n-1]*h/2)
            b[n-1] = -2*g(x[n-1]) + h**2*q(x[n-1])
            c[n-1] = 0
            d[n-1] = -(1*g(x[n-1]) + p(x[n-1])*h/2)*second_conditions[2]/second_conditions[1]
    else:
        print(60)
        a = [None] * (n-1)
        b = [None] * (n-1)
        c = [None] * (n-1)
        d = [0] * (n-1)
        a[0] = 0
        b[0] = -2+h**2*q(x[1])
        c[0] = 1 + p(x[1])*h/2
        d[0] = (p(x[1])*h/2-1)*first_conditions[2]/first_conditions[1]
        for i in range(1, n - 1):
            a[i] = 1*g(x[i]) - p(x[i]) * h / 2
            b[i] = -2*g(x[i]) + (h ** 2) * q(x[i])
            c[i] = 1*g(x[i]) + p(x[i]) * h / 2

        if second_conditions[0] != 0:
            a[n-2] = -second_conditions[0] / h
            b[n-2] = second_conditions[0] / h + second_conditions[1]
            c[n-2] = 0
            d[n-2] = second_conditions[2]
            print(75)
        else:
            a[n-2] = 1*g(x[n-1])-p(x[n-1]*h/2)
            b[n-2] = -2*g(x[n-1]) + h**2*q(x[n-1])
            c[n-2] = 0
            d[n-2] = -(1*g(x[n-1]) + p(x[n-1])*h/2)*second_conditions[2]/second_conditions[1]

    print("a:", a)
    print("b:", b)
    print("c:", c)
    print("d:", d)
    P, Q = straight_process(a, b, c, d)
    roots = reverse_process(P, Q)
    print(roots)
    print(y)
    return roots, x


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


def shooting_method(a, b):
    h = 0.01
    cur_pos = a
    x = []
    y = []
    while round(cur_pos, 6) <= b:
        x.append(cur_pos)
        cur_pos += h
    first_conditions = [0.5, 1, 4.5]
    second_conditions = [1, 0, 3-2*math.exp(-4)]
    right_derivative = second_conditions[2]/second_conditions[0]
    fst_derivatives = [1, 2]
    eps = 0.01

    penultimate_first_derivative = fst_derivatives[len(fst_derivatives) - 2]
    last_first_derivative = fst_derivatives[len(fst_derivatives) - 1]

    first_y = (first_conditions[2] - first_conditions[0] * penultimate_first_derivative) / first_conditions[1]
    y1, z1, delta_y1, delta_z1 = runge_kutt_method(x, h, first_y, penultimate_first_derivative)
    print(y1)
    print(z1)
    first_y = (first_conditions[2] - first_conditions[0] * last_first_derivative) / first_conditions[1]
    y2, z2, delta_y2, delta_z2 = runge_kutt_method(x, h, first_y, last_first_derivative)

    print(y2)
    print(z2)
    print("-"*10)
    y = np.copy(y2)
    fst_derivatives.append(last_first_derivative - (last_first_derivative - penultimate_first_derivative)*(z2[len(z2) - 1] - right_derivative)/
                           (z2[len(z2) - 1] - z1[len(z1) - 1]))
    print(fst_derivatives[len(fst_derivatives)-1])
    last_derivative = z2[len(z2)-1]

    while abs(last_derivative - right_derivative) > eps:
        first_y = (first_conditions[2]-first_conditions[0]*fst_derivatives[len(fst_derivatives)-1])/first_conditions[1]
        first_derivative = fst_derivatives[len(fst_derivatives)-1]

        cur_y, cur_z, delta_y, delta_z = runge_kutt_method(x, h, first_y, first_derivative)
        print(cur_y[len(cur_y)-1])
        print(cur_z[len(cur_z)-1])
        print("-"*10)
        penultimate_first_derivative = fst_derivatives[len(fst_derivatives)-2]
        last_first_derivative = fst_derivatives[len(fst_derivatives)-1]
        y = np.copy(cur_y)
        fst_derivatives.append(last_first_derivative - (last_first_derivative - penultimate_first_derivative)/
                               (cur_z[len(cur_z)-1] - last_derivative)*(cur_z[len(cur_z)-1]-right_derivative))
        print(last_derivative)
        last_derivative = cur_z[len(cur_z)-1]
    return y, x


if __name__=="__main__":
    start = 1
    finish = 2
    h = 0.01

    y, x = shooting_method(start, finish)
    table = PrettyTable()

    line0, = plt.plot(x, y, label="shooting method")
    y1, x1 = finite_difference_method(start, finish, h)
    p = 2
    print("-"*20, "Shooting method", "-"*20)
    table = PrettyTable()
    table._set_field_names(["k", "x", "y", "precise_y", "eps"])
    right_y = list(map(precise_y, x1))
    for i in range(len(x)-1):
        table.add_row([i, x[i], y[i], right_y[i], abs(y[i]-right_y[i])])
    print(table)

    table = PrettyTable()
    print("-"*20, "Finite difference method", "-"*20)
    table._set_field_names(["k", "x", "y", "precise_y", "eps"])
    for i in range(len(x1)):
        table.add_row([i, x1[i], y1[i], right_y[i], abs(y1[i]-right_y[i])])
    print(table)
    line1, = plt.plot(x1, right_y, label="y=3x+e^(-2x)")
    line2, = plt.plot(x1, y1, label="finite difference method")
    plt.legend(handles=[line0, line1, line2])
    plt.show()