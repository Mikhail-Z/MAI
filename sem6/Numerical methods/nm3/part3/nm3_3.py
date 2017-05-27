import numpy as np
import matplotlib.pyplot as plt


def F1(a, point_x):
    return np.sum(list(a[i]*point_x**i for i in range(len(a))))


if __name__=="__main__":
    x = [-0.7, -0.4, -0.1, 0.2, 0.5, 0.8]
    y = [-0.7754, -0.41152, -0.10017, 0.20136, 0.5236, 0.9273]
    #y = [0.0, 1.3038, 1.8439, 2.2583, 2.6077, 2.9155]
    #x = [0.0, 1.7, 3.4, 5.1, 6.8, 8.5]
    pow1 = 1
    pow2 = 2
    matrix_coef = np.zeros((pow1+1, pow1+1))
    b = np.zeros(pow1+1)
    N = len(x)-1
    for i in range(pow1+1):
        for j in range(pow1+1):
            matrix_coef[i, j] = np.sum(list(map(lambda a: a**(i+j), x)))
        b[i] = np.sum([y[k]*x[k]**i for k in range(len(x))])
    print("matr:\n{0}".format(matrix_coef))
    a = np.linalg.solve(matrix_coef, b)
    print("a:", a)
    y_vals_from_polynomial1 = list(F1(a, x[i]) for i in range(N+1))
    square_error_sum = np.sum(list((y_vals_from_polynomial1[i]-y[i])**2 for i in range(N+1)))
    print(square_error_sum)
    line1, = plt.plot(x, y_vals_from_polynomial1, label="y = {0}+{1}x".format(a[0], a[1]))
    print("-"*50)

    matrix_coef = np.zeros((pow2 + 1, pow2 + 1))
    b = np.zeros(pow2 + 1)
    N = len(x) - 1
    for i in range(pow2 + 1):
        for j in range(pow2 + 1):
            matrix_coef[i, j] = np.sum(list(map(lambda a: a ** (i + j), x)))
        b[i] = np.sum([y[k] * x[k] ** i for k in range(len(x))])
    print("matr:\n{0}".format(matrix_coef))
    a = np.linalg.solve(matrix_coef, b)
    print("a:", a)
    y_vals_from_polynomial2 = list(F1(a, x[i]) for i in range(N+1))
    line2, = plt.plot(x, y_vals_from_polynomial2, label="y = {0}+{1}x+{2}x^2".format(a[0], a[1], a[2]))
    plt.legend(handles=[line1, line2])
    plt.plot(x, y, "or")
    square_error_sum = np.sum(list((y_vals_from_polynomial2[i] - y[i]) ** 2 for i in range(N + 1)))
    print("Error", square_error_sum)
    plt.show()

