import os
import numpy as np
import logging
import sys

logging.basicConfig(format=u'%(funcName)s %(message)s', level=logging.DEBUG, filename=u'mylog.log', filemode='w')

num_of_permutations = 0


def load_data(filepath):
    list_of_coefficients = []
    list_of_free_members = []
    if os.path.exists(filepath):
        f = open(filepath)
        for line in f:
            line = line.split()
            numbers = [int(num) for num in line]
            list_of_coefficients.append(numbers[0:len(line)-1])
            list_of_free_members.append(numbers[len(numbers)-1])
        coefficients = np.matrix(list_of_coefficients)
        return coefficients, list_of_free_members
    else:
        return None


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


def preprocessing(coefficients, free_coefficients):
    global num_of_permutations
    size = len(coefficients)
    for i in range(len(coefficients)-1):
        if coefficients[i, i] == 0:
            permutation_row = permutation_of_rows(coefficients, size, free_coefficients, i)
            if permutation_row is None:
                print("Can't get bearing element")
                logging.error("Can't get bearing element\n")
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
        logging.info("step: {step}\t z[{i}]={z}\n".format(step=i, i=i, z=z[i]))
    print(z)
    for i in range(size-1, -1, -1):
        sum = 0
        for j in range(i+1, size):
            sum += round(U[i, j]*x[j], 3)
        x[i] = round((z[i]-sum)/U[i, i], 3)
        logging.info("step: {step}\t x[{i}]={x}\n".format(step=i, i=i, x=x[i]))

    return x


def get_inverse_matrix(matr):
    determinant = find_determinant(coefficients)
    logging.info("Determinant:{0}\n".format(determinant))
    transposed_matr = get_transposition_matr(matr)
    logging.info("Transposed matrix:\n{0}\n".format(transposed_matr))
    inverse_matr = transposed_matr/determinant
    logging.info("Inverse matrix:\n{0}\n".format(transposed_matr))
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
    if (len(sys.argv)== 2):
        filepath = sys.argv[1]
        coefficients, free_members = load_data(filepath)
        print(coefficients)
        print(free_members)
        if coefficients is None:
            print("No such file or directory")
            logging.error("No such file or directory")
    else:
        print("No input error")
        logging.error("No input file")
        sys.exit(1)
    logging.info("Coefficients in equations:\n{0}\n".format(coefficients))
    preprocessing(coefficients, free_members)
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
                    M[i, j] = round(-coefficients[i, k] / coefficients[k, k], 3)
                    reverse_M[i, j] = round(coefficients[i, k] / coefficients[k, k], 3)
                else:
                    M[i, j] = 0
                    reverse_M[i, j] = 0
        coefficients = M * coefficients
        L = L * reverse_M
        logging.info("k={step}\tCurrent M:\n{matr}\n".format(step=k, matr=M))
        logging.info("k={step}\tCurrent U:\n{matr}\n".format(step=k, matr=coefficients))
        logging.info("k={step}\tCurrent L:\n{matr}\n".format(step=k, matr=L))

    solution = linear_system_solution(L, coefficients, free_members)
    for root in solution:
        print("%.3f" %root)

    coefficients = L*coefficients  # снова получаем исходную матрицу
    logging.info("Coefficients check (L*U):\n{0}\n".format(coefficients))
    reverse_matrix = get_inverse_matrix(coefficients)
    print(reverse_matrix)
