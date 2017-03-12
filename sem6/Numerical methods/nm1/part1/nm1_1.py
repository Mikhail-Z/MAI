import os
import numpy as np
import logging
import sys

logging.basicConfig(format=u'%(funcName)s %(message)s', level=logging.DEBUG, filename=u'mylog.log', filemode='w')


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


def permutation_of_rows(coefficients, start, finish):
    for i in range(start, finish):
        if coefficients[i, i] != 0:
            tmp_row = coefficients[start]
            coefficients[start] = coefficients[i]
            coefficients[i] = tmp_row
            return i
    return None


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
    print(matr)
    size = len(matr)
    matr = np.concatenate((matr, np.eye(size)), axis=1)
    for i in range(size):
        if matr[i, i] == 0:
            index = find_i_of_max_elem(matr[:, i], i, size)
            permutation_of_rows(matr, i, index)
        for j in range(i+1, size):
            print(matr[j])
            matr[j] -= matr[j, i]* matr[i]/matr[i, i]
            print(matr[j])
            print("-"*10)
    print(matr)
    x = np.zeros((size, size))
    for i in range(size):
        x[size-1, i] = matr[size-1, size+i]/matr[size-1, size-1]
        for j in range(size-2, -1, -1):
            print("sum:",np.sum(list(map(lambda a, b: a*b, x[j+1:size, i], matr[j, j+1:size])))/matr[j, j])
            print(x[j+1:size, i], matr[j, j+1:size])
            x[j, i] = (matr[j, size + i] - np.sum(list(map(lambda a, b: a*b, x[j+1:size, i], matr[j, j+1:size]))))/matr[j, j]
    print(x)
    return x


def get_transposition_matr(matr):
    new_matr = np.copy(matr)
    size = len(matr)
    print(type(matr))
    row = np.array((size, 1))
    for i in range(size):
        row = matr[:, i]
        print("ROW:")
        print(row)
        print(new_matr[i, :])
        for j in range(size):
            new_matr[i, j] = row[j, 0]
    return new_matr


def find_i_of_max_elem(row, start, finish):
    max_elem = 0
    i_max = start
    for i in range(start, finish):
        if abs(row[i]) > max_elem:
            max_elem = abs(row[i])
            i_max = i
    if max_elem != 0:
        return i_max
    else:
        return None

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
                    if coefficients[k, k] == 0:
                        i_max = find_i_of_max_elem(coefficients[:, k], i+1, size)
                        if i_max is None:
                            print("Error")
                            sys.exit()
                        else:
                            print("NULL")
                            print(coefficients)
                            permutation_of_rows(coefficients, free_members, i, i_max)
                            print(coefficients)
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
    print("reversed matrix:")
    print(reverse_matrix)
