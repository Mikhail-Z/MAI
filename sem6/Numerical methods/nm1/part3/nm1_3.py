import os
import numpy as np
import logging
import sys

logging.basicConfig(format=u'%(message)s', level=logging.DEBUG, filename=u'mylog.log', filemode='w')

EPS = 0.001


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
        return list_of_coefficients, list_of_free_members
    else:
        return None


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        a, b = load_data(filepath)
        size = len(a)
        alpha = np.zeros((size, size))
        print(alpha)
        beta = np.zeros(size)
        for i in range(size):
            for j in range(size):
                if i != j:
                    alpha[i, j] = -a[i][j]/a[i][i]
                    logging.info("alpha[{i}][{j}]: {a}\n".format(i=i, j=j, a=alpha[i, j]))
            beta[i] = b[i]/a[i][i]
            logging.info("beta[{i}][{j}]: {b}\n".format(i=i, j=j, b=beta[i]))

        x = []
        x.append(np.empty(shape=(size, 1)))
        x[0] = np.array([beta[i] for i in range(size)])
        k = 1
        delta = EPS+1

        B = np.zeros((size, size))
        C = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                if i > j:
                    B[i][j] = alpha[i, j]
                else:
                    C[i][j] = alpha[i, j]
        logging.info("B:\n{0}\n".format(B))
        logging.info("C:\n{0}\n".format(C))
        while delta > EPS:
            logging.info("Iteration: {0}\n".format(k))
            logging.info("(E-B)^(-1)*C*x:\n{0}\n".format(np.dot(np.dot(np.linalg.inv(np.identity(size)-B), C), x[k-1])))
            logging.info("(E-B)^(-1)*beta:\n{0}\n".format(np.dot(np.linalg.inv(np.identity(size)-B), beta)))
            x.append(np.dot(np.dot(np.linalg.inv(np.identity(size)-B), C), x[k-1])
                     + np.dot(np.linalg.inv(np.identity(size)-B), beta))
            logging.info("x: {0}\n".format(x[k]))
            print("Iteration: {0}\n".format(k))
            print("x[{0}]: {1}\n".format(k, x[k]))
            delta = max(list(map(lambda a, b: abs(a-b), x[k], x[k-1])))
            logging.info("delta: {0}\n".format(delta))
            print("lambda: {0}\n".format(delta))
            k += 1