import numpy as np
import cmath
import os


def load_data(filepath):
    list_of_coefficients = []
    if os.path.exists(filepath):
        f = open(filepath)
        for line in f:
            line = line.split()
            numbers = [int(num) for num in line]
            list_of_coefficients.append(numbers[0:len(line)])
        coefficients = np.matrix(list_of_coefficients)
        return coefficients
    else:
        return None


def qr(A):
    m, n = A.shape
    Q = np.eye(m)
    for i in range(n - (m == n)):
        H = np.eye(m)
        H[i:, i:] = make_householder(A[i:, i])
        Q = np.dot(Q, H)
        A = np.dot(H, A)
    return Q, A


def make_householder(a):
    v = np.array([a[0] + np.copysign(np.linalg.norm(a), a[0])] + list(a[1:]))
    H = np.eye(a.shape[0])
    H -= (2 / np.dot(v, v)) * np.dot(v[:, None], v[None, :])
    '''v = a / (a[0] + np.copysign(np.linalg.norm(a), a[0]))
    v[0] = 1
    H = np.eye(a.shape[0])
    H -= (2 / np.dot(v, v)) * np.dot(v[:, None], v[None, :])'''
    return H


# task 1: show qr decomp of wp example
a = np.array(((
    (-9, 2, 2),
    (-2, 0, 7),
    (8, 2, 0),
)))

'''a = np.array(((
    (1, 3, 1),
    (1, 1, 4),
    (4, 3, 1),
)))'''
if __name__=="__main__":
    epsylon = 0.01
    eps = 0.01
    roots = []
    old_lambdas = []
    for k in range(0, 1000):
        print("k:", k)
        q, r = qr(a)
        print("q:")
        print(q)
        print("r:")
        print(r)
        new_q, new_r = np.linalg.qr(a)
        print("new_q:", new_q)
        print("new_r", new_r)
        a = np.dot(r, q)
        print("a:")
        print(a)
        real_less_than_eps = []
        for i in range(0, len(a)):
            real_less_than_eps.append(np.linalg.norm(a[i+1:, i]) < epsylon)
        cur_lambdas = []
        complex_less_than_eps = []
        for i in range(0, len(a)-1):
            b = a[i, i]+a[i+1, i+1]
            c = 4*(a[i, i]*a[i+1, i+1]-a[i, i+1]*a[i+1, i])
            D = b**2-4*c
            print("D:", D)
            lmbd1 = (-b + cmath.sqrt(D))/2
            lmbd2 = (-b - cmath.sqrt(D))/2
            cur_lambdas.append([lmbd1, lmbd2])
            print("lmbd: {0}".format(cur_lambdas[len(cur_lambdas)-1]))
            if k > 0 and D < 0:
                complex_less_than_eps.append(abs(cur_lambdas[i][0] - old_lambdas[i][0]) < eps and
                                            abs(cur_lambdas[i][1] - old_lambdas[i][1]) < eps)
            else:
                complex_less_than_eps.append(False)

        print(real_less_than_eps)
        old_lambdas = np.copy(cur_lambdas)
        num_of_roots = 0
        i = 0
        while i < len(a):
            print("i=", i)
            if real_less_than_eps[i]:
                num_of_roots += 1
                roots.append(a[i, i])
            elif i < len(a) - 1 and complex_less_than_eps[i]:
                num_of_roots += 2
                roots.append(cur_lambdas[i])
                i += 2
            i += 1
        print(num_of_roots)
        if num_of_roots == len(a):
            break
        else:
            roots.clear()
        print("------------------------")
    print(roots)
    print("+++++++++++++++")
    a1, b1 = np.linalg.eig(np.matrix([[-9, 2, 2], [-2, 0, 7], [8, 2, 0]]))
    #a2, b2 = np.linalg.eig(np.matrix([[1, 3, 1], [1, 1, 4], [4, 3, 1]]))
    print(a1)
    #print("*"*10)
    #print(a2)