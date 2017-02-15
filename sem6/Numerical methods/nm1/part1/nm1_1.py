import sys
import numpy as np

coefficients = np.matrix(
    [[10, 1, 1],
    [2, 10, 1],
    [2, 2, 10]]
)

size = len(coefficients)
num_of_permutations = 0

def permutation_if_rows(coefficients, start, finish=len(coefficients)):
    for i in range(start, finish):
        if coefficients[i, i] != 0:
            tmp = coefficients[start]
            coefficients[start] = coefficients[i]
            coefficients[i] = tmp
            return True
    return False


M = np.matrix(np.zeros((size, size)))

L = np.matrix(np.identity(size))

def error():
    print()
    sys.exit()


def preprocessing(coefficients):
    global num_of_permutations
    for i in range(len(coefficients)-1):
        if coefficients[i, i] == 0:
            if not permutation_if_rows(coefficients, i):
                error()
            else:
                num_of_permutations += 1

preprocessing(coefficients)
reverse_M = np.matrix(np.zeros((size, size)))

for k in range(size-1):
    for i in range(size):
        for j in range(size):
            if i == j:
                M[i, j] = 1
                reverse_M[i, j] = 1
            elif j == k and i > k:
                M[i, j] = -coefficients[i, k]/coefficients[k, k]
                reverse_M[i, j] = coefficients[i, k]/coefficients[k, k]
            else:
                M[i, j] = 0
                reverse_M[i, j] = 0

    coefficients = M*coefficients
    L = L*reverse_M

print(coefficients)
print(L)
print(L*coefficients)


def linear_system_solution(L, U, b):
    z = [None]*size
    x = [None]*size
    for i in range(size):
        sum = 0
        for j in range(i):
            sum += L[i, j]*z[j]
        z[i] = b[i] - sum
    print(z)
    for i in range(size-1, -1, -1):
        sum = 0
        for j in range(i+1, size):
            sum += U[i, j]*x[j]
        x[i] = 1/U[i, i]*(z[i]-sum)
    print(x)


linear_system_solution(L, coefficients, [12, 13, 14])

def get_inverse_matrix(matr):
    determinant = find_determinant(coefficients)
def transposition(matr, det):
    res_matrtmp_matr = matr

def find_determinant(U, num_of_permutations):
    k = (-1)**(num_of_permutations)
    determinant = 1
    for i in range(size):
        determinant *= U[i, i]
    return k*determinant

print(find_determinant(coefficients, num_of_permutations))