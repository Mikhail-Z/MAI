import numpy as np
import cmath
import os

a = 0
b = 1
eps = 0.01


def f(x):
    return np.log(x+1)-2*x**2+1


def f_derivative(x):
    return 1/(x+1)-4*x


def my_func_derivative(x):
    return 1/(2*cmath.sqrt((cmath.log(x+1)+1)/2))*(1/2*(-1/(x+1)))


def my_func_second_derivative(x):
    return -1/(x+1)**2-4


def my_func(x):
    return cmath.sqrt((cmath.log(x+1)+1)/2)


def simple_iteration_method():
    values_of_func = list()
    x = a
    while x < b:
        values_of_func.append(abs(my_func_derivative(x)))
        x += eps
    check_convergence = (np.amax(values_of_func) < 1)
    if check_convergence:
        x = 0
        q = np.amax(values_of_func)
        new_x = my_func(x)
        while new_x - x > q/(1-q)*abs(new_x - x):
            x = new_x
            new_x = my_func(x)
        print("Result: x={0}".format(new_x))


def newton_method():
    x = a
    while not f(x)*my_func_second_derivative(x) > 0:
        x += eps
    new_x = x - f(x)/f_derivative(x)
    print(x)
    while abs(new_x - x) < eps and x < b:
        x = new_x
        new_x = x - f(x)/f_derivative(x)
    print("Result: x={0}".format(new_x))


if __name__=="__main__":
    simple_iteration_method()
    newton_method()
