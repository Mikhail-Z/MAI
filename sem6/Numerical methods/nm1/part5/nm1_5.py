import numpy as np
import cmath


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
    '''v = np.array([a[0] + np.copysign(np.linalg.norm(a), a[0])] + list(a[1:]))
    H = np.eye(a.shape[0])
    H -= (2 / np.dot(v, v)) * np.dot(v[:, None], v[None, :])'''
    v = a / (a[0] + np.copysign(np.linalg.norm(a), a[0]))
    v[0] = 1
    H = np.eye(a.shape[0])
    H -= (2 / np.dot(v, v)) * np.dot(v[:, None], v[None, :])
    return H


# task 1: show qr decomp of wp example
a = np.array(((
    (1, 3, 1),
    (1, 1, 4),
    (4, 3, 1),
)))
epsylon = 0.01
roots = []
old_lambdas = []
for k in range(0, 10):
    print("k:", k)
    q, r = qr(a)
    a = r.dot(q)
    print("q:")
    print(q)
    print("r:")
    print(r)
    print("a:")
    print(a)
    real_less_than_eps = []
    print(np.linalg.norm(a[1:, 0]))
    for i in range(0, len(a)):
        real_less_than_eps.append(np.linalg.norm(a[i+1:, i]) < epsylon)
    cur_lambdas = []
    complex_less_than_eps = []
    for i in range(0, len(a)-1):
        b = a[i, i]+a[i+1, i+1]
        c = 4*(a[i, i]*a[i+1, i+1]-a[i, i+1]*a[i+1, i])
        D = b**2-4*c
        lmbd1 = (-b + cmath.sqrt(D))/2
        lmbd2 = (-b - cmath.sqrt(D))/2
        cur_lambdas.append([lmbd1, lmbd2])
        if k > 0:
            complex_less_than_eps.append(abs(cur_lambdas[i][0] - old_lambdas[i][0]) < epsylon and
                                        abs(cur_lambdas[i][1] - old_lambdas[i][1]) < epsylon)
        else:
            complex_less_than_eps.append(False)
    print(real_less_than_eps)
    num_of_roots = 0
    i = 0
    while i < len(a):
        print("i=", i)
        if i < len(a) - 1 and complex_less_than_eps[i]:
            num_of_roots += 2
            roots.append(cur_lambdas[i])
            i += 2
        elif real_less_than_eps[i]:
            num_of_roots += 1
            roots.append(a[i, i])
        i += 1
    print(num_of_roots)
    if num_of_roots == len(a):
        break
    else:
        old_lambdas = [lmbd for lmbd in cur_lambdas]
        roots.clear()
    print(cur_lambdas)
    print(old_lambdas)
    print("------------------------")
print(roots)
