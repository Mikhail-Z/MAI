import numpy as np
import sys
import os
from math import sqrt
import math


def load_data(filepath):
    list_of_coefficients = []
    if os.path.exists(filepath):
        f = open(filepath)
        for line in f:
            line = line.split()
            numbers = [int(num) for num in line]
            list_of_coefficients.append(numbers[0:len(line)-1])
        coefficients = np.matrix(list_of_coefficients)
        return coefficients
    else:
        return None


def rotation_method(a):
    n = len(a)
    max = abs(a[0, 1])
    i_max, j_max = 0, 1
    for i in range(n):
        for j in range(n):
            if i != j and abs(a[i, j]) > max:
                max = abs(a[i, j])
                i_max, j_max = i, j
    print("a:")
    print(a)
    print(i_max, j_max)
    U = np.matrix(np.eye(n, n))

    phi = 1/2*math.atan(2*a[i_max, j_max]/(a[i_max, i_max] - a[j_max, j_max]))
    U[i_max, i_max], U[j_max, j_max] = math.cos(phi), math.cos(phi)
    U[i_max, j_max], U[j_max, i_max] = -math.sin(phi), math.sin(phi)
    print("U:")
    print(U)
    a = U.transpose()*a*U
    return a, U

if __name__ == "__main__":
    a = np.array(((
        (4, 2, 1),
        (2, 5, 3),
        (1, 3, 6),
    )))
    sum = sys.maxsize
    n = len(a)
    eps = 0.3
    eigenvectors_matrix = np.matrix(np.eye(n))
    while sum > eps:
        a, U = rotation_method(a)
        eigenvectors_matrix = eigenvectors_matrix*U
        n = len(a)
        # sum = sqrt(sum([a[i, j] ** 2 for i in range(n) for j in range(n)]))
        sum = 0
        for i in range(n):
            for j in range(n):
                if j > i:
                    sum += a[i, j]**2
        sum = sqrt(sum)
        print(sum)
    eigenvalues = [a[i, i] for i in range(n)]
    eigenvectors = [eigenvectors_matrix[:, i] for i in range(n)]
    print(eigenvalues)
    print(eigenvectors)