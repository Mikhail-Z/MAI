import numpy as np


def straight_process(a, b, c, free_members):
    size = len(coefficients)
    P = [None] * size
    Q = [None] * size

    P[0] = -c[0] / b[0]
    Q[0] = free_members[0] / b[0]
    for i in range(1, size):
        P[i] = -c[i] / (b[i] + a[i] * P[i - 1])
        Q[i] = (free_members[i] - c[i] * Q[i - 1]) / (b[i] + c[i] * P[i - 1])
    return P, Q


def reverse_process(P, Q):
    size = len(P)
    x = [None] * size
    x[size-1] = Q[size-1]
    for i in range(size-2, -1, -1):
        x[i] = P[i]*x[i+1] + Q[i]
    return x

if __name__ == "__main__":
    coefficients = np.matrix(
        [[8, -2, 0, 0],
         [-1, 6, -2, 0],
         [0, 2, 10, -4],
         [0, 0, -1, 6]]
    )
    a = [0, -1, 2, -1]
    b = [8, 6, 10, 6]
    c = [-2, -2, -2, 0]
    free_members = [6, 3, 8, 5]
    P, Q = straight_process(a, b, c, free_members)
    roots = reverse_process(P, Q)
    print(roots)
