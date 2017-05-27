import numpy as np
from prettytable import PrettyTable


def f(x):
    return 1/(x**2 + 4)


def rectangle_method(x, h):
    res = 0
    intermediate_results = [res]
    for i in range(1, len(x)):
        res += h*f((x[i] + x[i-1])/2)
        intermediate_results.append(res)
    return intermediate_results


def trapezoid_method(x, h):
    res = 0
    intermediate_results = [res]
    for i in range(1, len(x)):
        res += 0.5 * h * (f(x[i]) + f(x[i - 1]))
        intermediate_results.append(res)
    return intermediate_results


def simpson_method(x, h):
    res = 1/3*h*f(x[0])
    intermediate_results = [res]
    for i in range(1, len(x)-1):
        if i % 2:
            res += 1/3*h*4*f(x[i])
        else:
            res += 1/3*h*2*f(x[i])
        intermediate_results.append(res)
    res += 1/3*h*f(x[len(x)-1])
    intermediate_results.append(res)
    return intermediate_results


def runge_rumberg_method(h1_res, h2_res, h1, h2):
    results = []
    for i in range(len(h1_res)):
        if 0 <= i < 2: # метод трапеций или прямоугольника
            results.append(h2_res[i] + (h2_res[i] - h1_res[i])/((h1/h2)**2-1))
        else: # метод симпсона
            results.append(h2_res[i] + (h2_res[i] - h1_res[i]) / ((h1 / h2) ** 4 - 1))
    return results


if __name__ == "__main__":
    start = -2.
    finish = 2.
    h1 = 1
    h2 = 0.5
    step = start
    x = list()
    while step <= finish:
        x.append(step)
        step += h1
    y = []
    for i in range(len(x)):
        y.append(f(x[i]))
    table = PrettyTable()
    table._set_field_names(["step", "x", "y", "rectangle method", "trapezoid method", "simpson method"])
    h1_res = [rectangle_method(x, h1), trapezoid_method(x, h1), simpson_method(x, h1)]
    for i in range(len(x)):
        table.add_row([i, x[i], y[i]] + [h1_res[j][i] for j in range(len(h1_res))])
    h1_res = np.array(h1_res)[:, len(x)-1]
    print(table)

    step = start
    x = list()
    while step <= finish:
        x.append(step)
        step += h2
    y = []
    for i in range(len(x)):
        y.append(f(x[i]))
    table = PrettyTable()
    table._set_field_names(["step", "x", "y", "rectangle method", "trapezoid method", "simpson method"])
    h2_res = [rectangle_method(x, h2), trapezoid_method(x, h2), simpson_method(x, h2)]
    for i in range(len(x)):
        table.add_row([i, x[i], y[i]] + [h2_res[j][i] for j in range(len(h2_res))])
    h2_res = np.array(h2_res)[:, len(x) - 1]
    print(table)
    print("\nabsolute error")
    table = PrettyTable()
    table._set_field_names(["f(x)", "precise value", "runge_rumberg_method (rectangle)", "runge_rumberg (trapezoid)",
                            "runge_rumberg (simpson)", "err rectangle method", "err trapezoid method", "err simpson method"])
    precise_value = 0.78540
    most_precise_vals = runge_rumberg_method(h1_res, h2_res, h1, h2)
    table.add_row(["1/(x**2+ 4)", precise_value, most_precise_vals[0], most_precise_vals[1],
                   most_precise_vals[2], abs(most_precise_vals[0] - precise_value),
                   abs(most_precise_vals[1] - precise_value), abs(most_precise_vals[2] - precise_value)])
    print(table)
