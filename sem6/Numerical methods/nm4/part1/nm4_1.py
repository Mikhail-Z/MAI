import numpy as np
import math
from prettytable import PrettyTable
import matplotlib.pyplot as plt


def f(x, y, z):
    return 4*x*z + math.exp(x**2) - (4*x**2 - 3)*y
    #return z/x**0.5-y/(4*x**2)*(x+x**0.5-8)

def y_func(x):
    return (math.exp(x) + math.exp(-x) - 1)*math.exp(x**2)
    #return (x**2+1/x)*math.exp(x**0.5)

def eiler_method(start, finish, step, first_y, first_z):
    i = 0
    x = [start]
    y = [first_y]
    z = [first_z]
    cur_pos = start
    cur_pos += step
    while round(cur_pos, 6) <= finish:
        x.append(cur_pos)
        y.append(y[i] + step * z[i])
        z.append(z[i] + step * f(cur_pos, y[i], z[i]))
        cur_pos += step
        i += 1
    return y, z

def adams_method(start, finish, first_y, first_z, step):
    cur_pos = start
    i = 0
    x = []
    while cur_pos <= finish and i < 4:
        x.append(cur_pos)
        cur_pos += step
        i += 1
    y, z, delta_y, delta_z = runge_kutt_method(x, step, first_y, first_z)

    while round(cur_pos, 4) <= finish:
        x.append(cur_pos)
        cur_pos += step
    while i < len(x):
        y.append(y[i-1] + step/24*(55*z[i-1] - 59*z[i-2] + 37*z[i-3] - 9*z[i-4]))
        z.append(z[i-1] + step/24*(55*f(x[i-1], y[i-1], z[i-1]) - 59*f(x[i-2], y[i-2], z[i-2]) +
                                   37*f(x[i-3], y[i-3], z[i-3]) - 9*f(x[i-4], y[i-4], z[i-4])))
        i += 1
    return y


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


if __name__ == "__main__":
    step = 0.1
    start = 0
    finish = 1
    y_first = 1
    z_first = 0
    x = []
    cur_pos = start
    while round(cur_pos, 6) <= finish:
        x.append(cur_pos)
        cur_pos += step
    y1 = adams_method(start, finish, y_first, z_first, step)
    y2 = adams_method(start, finish, y_first, z_first, 0.5*step)
    print("-" * 50, "Adams method", "-" * 50)
    p = 2
    table = PrettyTable()
    table._set_field_names(["k", "x", "y", "precise y", "eps", "runge romberg precision"])
    for i in range(len(x)):
        table.add_row([i, x[i], y1[i], y_func(x[i]), abs(y1[i] - y_func(x[i])), abs(y1[i]-y2[i*2])/(2**p-1)])
    print(table)
    print()
    line1, = plt.plot(x, y1, label="Adams method")


    print("-" * 50, "Eiler method", "-" * 50)
    p = 2
    y1, z1 = eiler_method(start, finish, step, y_first, z_first)
    y2, z2 = eiler_method(start, finish, 0.5 * step, y_first, z_first)
    line2, = plt.plot(x, y1, label="Eiler method")
    table = PrettyTable()
    table._set_field_names(["k", "x", "y", "precise y", "eps", "runge romberg precision"])
    for i in range(len(x)):
        table.add_row([i, x[i], y1[i], y_func(x[i]), abs(y1[i] - y_func(x[i])), abs(y2[2*i]-y1[i])/(2**p-1)])
    print(table)
    print()


    cur_pos = start
    x1 = []
    while round(cur_pos, 6) <= finish:
        x1.append(cur_pos)
        cur_pos += 0.5 * step
    y1, z1, delta_y1, delta_z1 = runge_kutt_method(x, step, y_first, z_first)
    y2, z2, delta_y2, delta_z2 = runge_kutt_method(x1, 0.5*step, y_first, z_first)
    line3, = plt.plot(x, y1, label="Runge Kutt method")
    right_y = list(map(y_func, x))
    line4, = plt.plot(x, right_y, label="(e^x+e^(-x)-1)*e^(x^2)")
    table = PrettyTable()
    print(" "*50, "runge kutt method")
    p = 4
    table._set_field_names(["k", "x", "y", "delta y", "delta z", "precise y", "eps", "runge romberg precision"])
    for i in range(len(x)):
        table.add_row([i, x[i], y1[i], delta_y1[i], delta_z1[i], y_func(x[i]), abs(y1[i]-y_func(x[i])), abs((y2[i*2]-y1[i])/(2**p-1))])
    print(table)
    plt.legend(handles=[line1, line2, line3, line4])
    plt.show()