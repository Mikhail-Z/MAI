import sys
import numpy as np

coefficients = np.matrix(
    [[10, 1, 1],
    [2, 10, 1],
    [2, 2, 10]]
)

size = len(coefficients)


def permutation_if_rows(coefficients, start, finish=len(coefficients)):
    for i in range(start, finish):
        if coefficients[i, i] != 0:
            tmp = coefficients[start]
            coefficients[start] = coefficients[i]
            coefficients[i] = tmp
            return True
    return False


M = np.ones((size, size))

for i in range(size):
    np.append(M, [[0 for i in range(size)]])

L = np.ones((size, size))
L.fill(1)

def error():
    print()
    sys.exit()


def preprocessing(coefficients):
    for i in range(len(coefficients)-1):
        if coefficients[i, i] == 0:
            if not permutation_if_rows(coefficients, i):
                error()


preprocessing(coefficients)
for k in range(size-1):
    for i in range(size):
        for j in range(size):
            if i == j:
                M[i, j] = 1
            elif i != j and j == k:
                M[i, j] = -coefficients[i, k]/coefficients[k, k]
            else:
                M[i, j] = 0
    coefficients = M*coefficients
    L = L*M
print(coefficients)