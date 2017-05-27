import numpy as np
import math
import functools
from prettytable import PrettyTable


def my_func(x):
   return math.sin(x)

def f(x, y, idx):
    n = len(idx)
    if n > 2:
        res = (f(x, y, idx[0:n-1]) - f(x, y, idx[1:n]))/(x[idx[0]]-x[idx[n-1]])
        print("f({0})".format(idx))
        print(res)
        return res
    else:
        i = idx[0]
        j = idx[1]
        print("f({0})".format(idx))
        res = (y[i]-y[j])/(x[i]-x[j])
        print(res)
        return res


def w(x, i):
    return functools.reduce(lambda a, b: a*b, [(x[i]-x[j]) for j in range(len(x)) if j != i])


def L(x_vals, w_vals, point):
    n = len(x_vals)
    return sum([my_func(x_vals[j])/w_vals[j]*functools.reduce(lambda a, b: a*b, [(point-x_vals[i])
                                                       for i in range(n) if i != j]) for j in range(n)])


def P(x_vals, y_vals, X):
    n = len(x_vals)
    print(x_vals)
    tmp_res = my_func(x_vals[0])
    for i in range(1, n):
        print("-"*50)
        idx = list(range(i+1))
        print(idx)
        print("-"*50)
        tmp_res += functools.reduce(lambda a, b: a*b, [X-x_vals[j] for j in range(i)]) * f(x_vals, y_vals, idx)
    print("Result:", tmp_res)
    return tmp_res


if __name__=="__main__":
    print("*******f(x) = arcsin(x)**********")
    X = 0.1
    #X = 1.5
    x_vals = [-0.4, -0.1, 0.2, 0.5]
    #x_vals = [0, 1, 2, 3]
    y_vals = list(map(my_func, x_vals))
    n = len(x_vals)
    w_vals = [w(x_vals, i) for i in range(n)]
    print("{0}Lagrange interpolation method{1}".format("-"*10, "-"*10))
    table = PrettyTable()
    table._set_field_names(["i", "x[i]", "f[i]", "w'[i]", "f[i]/w'[i]", "X* - x[i]"])

    for i in range(n):
        table.add_row([i, x_vals[i], y_vals[i], w(x_vals, i), y_vals[i]/w(x_vals, i), X-x_vals[i]])
    print(table)
    print()

    func = "arcsin(x)"
    print("X*: {0}, Lagrange_polynomial: {1}, {2}: {3}):".format(X, L(x_vals, w_vals, X), func, my_func(X)))
    print("absolute error: ", abs(L(x_vals, w_vals, X) - my_func(X)))

    print("\n")

    #x_vals = [-0.4, -0.1, 0.2, 0.5]
    #y_vals = list(map(my_func, x_vals))
    print("{0}Newton interpolation method{1}".format("-"*10, "-"*10))
    print("x:", x_vals)
    print("y:", y_vals)
    #print(P(x_vals, y_vals, X))
    print("absolute error: ", abs(P(x_vals, y_vals, X) - my_func(X)))