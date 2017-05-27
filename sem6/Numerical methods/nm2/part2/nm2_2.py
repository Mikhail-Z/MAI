import numpy as np
import math
import sys


a = 3
eps = 0.0001
start = 2.12
finish = 2.12

def f1(x):
    return x[0]**2+x[1]**2-a**2

def f2(x):
    return x[0] - math.exp(x[1]) + a

def f1_derivative_x1(x):
    return 2*x[0]

def f1_derivative_x2(x):
    return 2*x[1]

def f2_derivative_x1(x):
    return 1

def f2_derivative_x2(x):
    return -math.exp(x[1])

def det_A1(x):
    return f1(x)*f2_derivative_x2(x)-f2(x)*f1_derivative_x2(x)

def det_A2(x):
    return f1_derivative_x1(x)*f2(x)-f2_derivative_x1(x)*f1(x)

def det_J(x):
    return f1_derivative_x1(x)*f2_derivative_x2(x)-f2_derivative_x1(x)*f1_derivative_x2(x)

def newton_method():
    x = [start, finish]
    print("x1: {0}, x2: {1}".format(x[0], x[1]))
    new_x = [None, None]
    i = 0
    try:
        i += 1
        new_x[0] = x[0] - det_A1(x) / det_J(x)
        new_x[1] = x[1] - det_A2(x) / det_J(x)
        while np.amax([abs(new_x[0] - x[0]), abs(new_x[1] - x[1])]) >= eps:
            i += 1
            x = new_x.copy()
            print("x1: {0}, x2: {1}".format(x[0], x[1]))
            new_x[0] = x[0] - det_A1(x) / det_J(x)
            new_x[1] = x[1] - det_A2(x) / det_J(x)
    except ZeroDivisionError:
        print("Nondegeneracy of the Jacobi matrix is not satisfied!")
        sys.exit(1)
    print("num of iterations:", i)
    return new_x

def phi1(x):
    return math.sqrt(9-x[1]**2)

def phi2(x):
    return math.log(x[0]+3)

def phi1_derivative_x2(x):
    return -2*x[1]/math.sqrt(a**2-x[1]**2)

def phi1_derivative_x1(x):
    return 0

def phi2_derivative_x1(x):
    return 1/(x[0]+a)

def phi2_derivative_x2(x):
    return 0

def convergence_check(x):
    size = len(x)
    jacobi_matr = np.empty(shape=(size, size))
    jacobi_matr[0, 0] = phi1_derivative_x1(x)
    jacobi_matr[0, 1] = phi1_derivative_x2(x)
    jacobi_matr[1, 0] = phi2_derivative_x1(x)
    jacobi_matr[1, 1] = phi2_derivative_x2(x)
    q = np.amax(jacobi_matr)
    if abs(q) < 1:
        return abs(q)
    else:
        return None


def simple_iteration_method():
    x = [None, None]
    x[0], x[1] = start, finish
    print("x1: {0}, x2: {1}".format(x[0], x[1]))
    q = convergence_check(x)
    new_x = [None, None]
    i = 0
    if q is not None:
        i += 1
        new_x[0] = phi1(x)
        new_x[1] = phi2(x)
        print("x1: {0}, x2: {1}".format(new_x[0], new_x[1]))
        while max(abs(new_x[0]-x[0]), ab
        +s(new_x[1]-x[1])) >= eps:
            i += 1
            x = np.copy(new_x)
            new_x[0] = phi1(x)
            new_x[1] = phi2(x)
            print(new_x)
        print("num of iterations:", i)
        return new_x
    else:
        print("Convergence condition doesn't perform!")
        return None


if __name__=="__main__":
    print("-----Newton method-----")
    x = newton_method()
    if x is not None:
        print("Result: x =", x)
    print("-----Simple iteration method-----")
    x = simple_iteration_method()
    if x is not None:
        print("Result: x =", x)