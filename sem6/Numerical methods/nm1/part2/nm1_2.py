import numpy as np
import logging
import sys
import os
logging.basicConfig(format=u'%(message)s', level=logging.DEBUG, filename=u'mylog.log', filemode='w')


def load_data(filepath):
    a, b, c, d = [], [], [], []
    if os.path.exists(filepath):
        f = open(filepath)
        for line in f:
            line = line.split()
            numbers = [int(num) for num in line]
            a.append(numbers[0])
            b.append(numbers[1])
            c.append(numbers[2])
            d.append(numbers[3])
        return a, b, c, d
    else:
        return None


def straight_process(a, b, c, free_members):
    size = len(free_members)
    P = [None] * size
    Q = [None] * size

    P[0] = -c[0] / b[0]
    Q[0] = free_members[0] / b[0]
    logging.info("P[0]:%d, Q[0]:%d" %(P[0], Q[0]))
    for i in range(1, size):
        P[i] = -c[i] / (b[i] + a[i] * P[i - 1])
        Q[i] = (free_members[i] - a[i] * Q[i - 1]) / (b[i] + a[i] * P[i - 1])
        logging.info("P[%d]:%d, Q[%d]:%d" % (i, P[0], i, Q[0]))
    return P, Q


def reverse_process(P, Q):
    size = len(P)
    x = [None] * size
    x[size-1] = Q[size-1]
    for i in range(size-2, -1, -1):
        x[i] = P[i]*x[i+1] + Q[i]
    return x

if __name__ == "__main__":
    if (len(sys.argv)== 2):
        filepath = sys.argv[1]
        a, b, c, d = load_data(filepath)
        if a is None:
            print("No such file or directory")
            logging.error("No such file or directory")
    else:
        print("No input error")
        logging.error("No input file")
        sys.exit(1)
    P, Q = straight_process(a, b, c, d)
    roots = reverse_process(P, Q)
    print(roots)
    logging.info("roots:{0}".format(roots))
