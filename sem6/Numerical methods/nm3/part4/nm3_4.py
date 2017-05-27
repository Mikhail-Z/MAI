import numpy as np
from sys import exit


X = 1.


def get_first_derivative(x, y, seg_num):
    return (y[seg_num + 1] - y[seg_num])/(x[seg_num + 1] - x[seg_num])


def get_second_derivative(x, y, seg_num):
    return 2*(get_first_derivative(x, y, segment_num + 1) - get_first_derivative(x, y, segment_num))/\
           (x[seg_num+2] - x[seg_num])


if __name__ == "__main__":
    x = [-1., 0., 1., 2., 3.]
    y = [-0.7854, 0.0, 0.78540, 1.1071, 1.249]
    segment_num = -1
    i = 0
    while i + 1 < len(x) and x[i + 1] < X:
        i += 1

    segment_num = i
    print("segment number:", segment_num)
    if segment_num + 1 < len(x):
        if X == x[segment_num + 1]:
            if 0 < segment_num < (len(x)) - 1:
                left_derivative = get_first_derivative(x, y, segment_num)
                right_derivative = get_first_derivative(x, y, segment_num + 1)
                derivative = (right_derivative + left_derivative) / 2
                print("first derivative:")
                print(derivative)
                second_derivative = get_second_derivative(x, y, segment_num)
                print("second derivative:")
                print(second_derivative)
        else:
            derivative = get_first_derivative(x, y, segment_num)
            print("first derivative:")
            print(derivative)
            if segment_num + 2 < len(x):
                second_derivative = get_second_derivative(x, y, segment_num)
                print(second_derivative)
                print("second derivative:")
                print(second_derivative)

