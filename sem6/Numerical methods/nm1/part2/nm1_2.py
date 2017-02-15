import numpy as np


def straight_process(coefficients, free_members):
    size = len(coefficients)
    P = [None] * size
    Q = [None] * size

    P[0] = -coefficients[0, 2] / coefficients[0, 1]
    Q[0] = free_members[0] / coefficients[1]
    for i in range(1, size):
        P[i] = -coefficients[i, 2] / (coefficients[i, 1] + coefficients[i, 0] * P[i - 1])
        Q[i] = (free_members[i] - coefficients[i, 0] * Q[i - 1]) / (coefficients[i, 1] + coefficients[i, 0] * P[i - 1])
    return P, Q


if __name__ == "__main__":
    coefficients = np.matrix(
        [[8, -2, 0, 0],
         [-1, 6, -2, 0],
         [0, 2, 10, -4],
         [0, 0, -1, 6]]
    )
    free_members = [6, 3, 8, 5]
    straight_process(coefficients, free_members)
    reverse_process(P, Q)
