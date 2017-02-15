import sys
import numpy as np


num_of_permutations = 0


def permutation_of_rows(coefficients, free_coefficients, start, finish):
    for i in range(start, finish):
        if coefficients[i, i] != 0:
            tmp_row = coefficients[start]
            tmp_free_member = free_coefficients[start]
            coefficients[start] = coefficients[i]
            coefficients[i] = tmp_row
            free_coefficients[start] = free_coefficients[i]
            free_coefficients[i] = tmp_free_member
            return i
    return None


def error():
    print()
    sys.exit()


def preprocessing(coefficients, free_coefficients):
    global num_of_permutations
    size = len(coefficients)
    for i in range(len(coefficients)-1):
        if coefficients[i, i] == 0:
            permutation_row = permutation_of_rows(coefficients, size, free_coefficients, i)
            if permutation_row is None:
                error()
            else:
                num_of_permutations += 1


def linear_system_solution(L, U, b):
    z = [None]*size
    x = [None]*size
    for i in range(size):
        sum = 0
        for j in range(i):
            sum += L[i, j]*z[j]
        z[i] = b[i] - sum
    for i in range(size-1, -1, -1):
        sum = 0
        for j in range(i+1, size):
            sum += U[i, j]*x[j]
        x[i] = 1/U[i, i]*(z[i]-sum)
    return x


def get_inverse_matrix(matr):
    determinant = find_determinant(coefficients)
    transposed_matr = get_transposition_matr(matr)
    inverse_matr = transposed_matr/determinant
    return inverse_matr


def get_transposition_matr(matr):
    new_matr = np.copy(matr)
    size = len(matr)
    row = [None]*size
    for i in range(size-1, -1, -1):
        for j in range(size):
            row[j] = matr[j, i]
        new_matr[size-i-1] = row
    return new_matr


def find_determinant(U):
    k = (-1)**(num_of_permutations)
    determinant = 1
    for i in range(size):
        determinant *= U[i, i]
    return k*determinant

if __name__ == "__main__":
    coefficients = np.matrix(
        [[10, 1, 1],
         [2, 10, 1],
         [2, 2, 10]]
    )
    free_coefficients = [12, 13, 14]
    preprocessing(coefficients, free_coefficients)
    size = len(coefficients)
    M = np.matrix(np.zeros((size, size)))
    L = np.matrix(np.identity(size))

    reverse_M = np.matrix(np.zeros((size, size)))

    for k in range(size - 1):
        for i in range(size):
            for j in range(size):
                if i == j:
                    M[i, j] = 1
                    reverse_M[i, j] = 1
                elif j == k and i > k:
                    M[i, j] = -coefficients[i, k] / coefficients[k, k]
                    reverse_M[i, j] = coefficients[i, k] / coefficients[k, k]
                else:
                    M[i, j] = 0
                    reverse_M[i, j] = 0

        coefficients = M * coefficients
        L = L * reverse_M

    coefficients = L*coefficients
    solution = linear_system_solution(L, coefficients, free_coefficients)
    print(solution)

    reverse_matrix = get_inverse_matrix(coefficients)
    print(reverse_matrix)
