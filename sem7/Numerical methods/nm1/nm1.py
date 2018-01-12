import numpy as np
import matplotlib.pyplot as plt



def term1(t):
    return np.sin(t)


def term2(t):
    return -np.sin(t)


def term3(x):
    return 0


def f(x, t):
    return np.sin(t)*np.cos(x)


def additional_member(t, x):
    return np.cos(x) * (np.sin(t) + np.cos(t))


def solve(a, b, c, d, n):
    P = np.empty(n)
    Q = np.empty(n)
    P[0] = -c[0]/b[0]
    Q[0] = d[0]/b[0]
    k = n - 1
    for i in range(1, k):
        P[i] = -c[i]/(b[i] + a[i]*P[i-1])
        Q[i] = (d[i] - a[i]*Q[i-1])/(b[i] + a[i]*P[i-1])
    P[k] = 0
    Q[k] = (d[k] - a[k]*Q[k-1])/(b[k]+a[k]*P[k-1])

    x = np.empty(n)
    x[k] = Q[k]
    for i in range(1, n):
        x[k - i] = P[k-i]*x[k - i + 1] + Q[k-i]
    return x

# -------------------------------------------------------------------------------------------------


def expl_fin_dif_scheme_appr1(u, tay, h, m, n):
    time = 0
    for i in range(1, m):
        for j in range(1, n - 1):
            u[i][j] = tay * (u[i - 1][j + 1] - 2 * u[i - 1][j] + u[i - 1][j - 1]) / h ** 2 + \
                      u[i - 1][j] + tay * additional_member(time, h * j)
        u[i][n - 1] = u[i][n - 2] + term2(time) * h
        time += tay


def expl_fin_dif_scheme_appr2(u, tay, h, m, n):
    time = 0
    for i in range(1, m):
        for j in range(1, n - 1):
            u[i][j] = tay * (u[i - 1][j + 1] - 2 * u[i - 1][j] + u[i - 1][j - 1]) / h ** 2 + \
                      u[i - 1][j] + tay * additional_member(time, h * j)
        u[i][n - 1] = (term2(time) * 2 * h - u[i][n - 3] + 4 * u[i][n - 2]) / 3
        time += tay


def expl_fin_dif_scheme_appr3(u, tay, h, m, n):
    time = 0
    for i in range(1, m):
        for j in range(1, n - 1):
            u[i][j] = tay * (u[i - 1][j + 1] - 2 * u[i - 1][j] + u[i - 1][j - 1]) / h ** 2 + \
                      u[i - 1][j] + tay * additional_member(time, h * j)
        u[i][n - 1] = (term2(time) + 1 / h * u[i][n - 2] + h / (2 * tay) * u[i - 1][n - 1]) / (1 / h + h / (2 * tay))
        time += tay



# -----------------------------------------------------------------------------------------------------------

def impl_fin_dif_scheme_appr1(u, tay, h, m, n, par_a):
    time = 0
    for k in range(m - 1):
        a = np.empty(n)
        b = np.empty(n)
        c = np.empty(n)
        d = np.empty(n)
        sigma = (par_a ** 2 * tay) / (h ** 2)

        a[0] = 0
        b[0] = -(1 + 2 * sigma)
        c[0] = sigma
        d[0] = -u[k][0] - sigma * term1((k + 1) * tay) - tay * additional_member(time, 0 * h)
        for j in range(1, n - 1):
            a[j] = sigma
            b[j] = -(1 + 2 * sigma)
            c[j] = sigma
            d[j] = -u[k][j] - tay * additional_member(time, j * h)
        a[n - 1] = -1 / h
        b[n - 1] = 1 / h
        c[n - 1] = 0

        d[n - 1] = term2(time)
        '''print("Условие устойчивости")
        for i in range(n):
            print(a[i] + c[i] < b[i])
        print('-' * 50)'''
        Y = solve(a, b, c, d, n)

        for i in range(n):
            u[k + 1][i] = Y[i]
        time += tay


def impl_fin_dif_scheme_appr2(u, tay, h, m, n, par_a):
    print(m, n)
    time = 0
    for k in range(m - 1):
        a = np.empty(n)
        b = np.empty(n)
        c = np.empty(n)
        d = np.empty(n)
        sigma = (par_a ** 2 * tay) / (h ** 2)

        a[0] = 0
        b[0] = -(1 + 2 * sigma)
        c[0] = sigma
        d[0] = -u[k][0] - sigma * term1((k + 1) * tay) - tay * additional_member(time, 0 * h)
        for j in range(1, n-1):
            a[j] = sigma
            b[j] = -(1 + 2 * sigma)
            c[j] = sigma
            d[j] = -u[k][j] - tay * additional_member(time, j * h)

        coef = (-1 / (2 * h)) / a[n - 2]
        abcd = np.array([a[n - 2] * coef + 1 / (2 * h), b[n - 2] * coef - 4 / (2 * h), c[n - 2] * coef + 3 / (2 * h),
                         d[n - 2] * coef + term2(time)])
        c[n-1] = abcd[0]
        a[n-1] = abcd[1]
        b[n-1] = abcd[2]
        d[n-1] = abcd[3]
        print('a[n-1],b[n-1],c[n-1],d[n-1]', a[n-1], b[n-1], c[n-1], d[n-1])
        '''a[n - 1] = a[n - 2] * ((-1 / (2 * h)) / a[n - 2]) + 1 / (2 * h)
        b[n - 1] = b[n - 2] * ((-1 / (2 * h)) / a[n - 2]) - 4 / (2 * h)
        c[n - 1] = c[n - 2] * ((-1 / (2 * h)) / a[n - 2]) + 3 / (2 * h)
        d[n - 1] = d[n - 2] * ((-1 / (2 * h)) / a[n - 2]) + term2(time)'''
        #print(a[n - 1], b[n - 1])
        Y = solve(a, b, c, d, n)
        '''print("Условие устойчивости")
        for i in range(n):
            print(a[i] + c[i] < b[i])
        print('-' * 50)'''
        for i in range(n):
            u[k + 1][i] = Y[i]
        time += tay


def impl_fin_dif_scheme_appr3(u, tay, h, m, n, par_a):
    time = 0
    for k in range(m - 1):
        a = np.empty(n)
        b = np.empty(n)
        c = np.empty(n)
        d = np.empty(n)
        sigma = (par_a ** 2 * tay) / (h ** 2)

        a[0] = 0
        b[0] = -(1 + sigma)
        c[0] = sigma / 2
        d[0] = -((1 - sigma) * u[k][1] + sigma / 2 * u[k][0]) - tay * additional_member(time, 0 * h) - sigma * term1(
            (k + 1) * tay)
        for j in range(1, n - 1):
            a[j] = sigma / 2
            b[j] = -(1 + sigma)
            c[j] = sigma / 2
            d[j] = -(
            sigma / 2 * u[k][j - 1] + (1 - sigma) * u[k][j] + sigma / 2 * u[k][j + 1]) - tay * additional_member(time, j * h)

        a[n-1] = -1/h
        b[n-1] = (1/h+h/(2*tay))
        c[n-1] = 0
        d[n-1] = term2(time) + additional_member(time, (n-1)*h)/h + h/(2*tay)*u[k, n-1]
        '''a[n - 1] = -2 / h
        b[n - 1] = 2 / h + h / tay
        c[n - 1] = 0
        d[n - 1] = h / tay * u[n - 2][n - 1] + 2 * term2((k + 1) * tay)'''
        '''print("Условие устойчивости")
        for i in range(n):
            print(a[i] + c[i] < b[i])
        print('-'*50)'''
        Y = solve(a, b, c, d, n)
        for i in range(n):
            u[k + 1][i] = Y[i]
        time += tay

# --------------------------------------------------------------------------------------------------------

def expl_impl_fin_dif_scheme_appr1(u, tay, h, m, n, par_a):
    time = 0
    for k in range(m - 1):
        a = np.empty(n)
        b = np.empty(n)
        c = np.empty(n)
        d = np.empty(n)
        sigma = (par_a ** 2 * tay) / (h ** 2)

        a[0] = 0
        b[0] = -(1 + sigma)
        c[0] = sigma / 2
        d[0] = -(sigma / 2 * term1(k*tay) + (1 - sigma) * u[k][0] + sigma / 2 * u[k][1]) -\
               tay * additional_member(time, 0 * h) - 0.5*sigma * term1((k + 1) * tay)
        for j in range(1, n - 1):
            a[j] = sigma / 2
            b[j] = -(1 + sigma)
            c[j] = sigma / 2
            d[j] = -(sigma / 2 * u[k][j - 1] + (1 - sigma) * u[k][j] + sigma / 2 * u[k][j + 1])\
                   - tay * additional_member(time, j * h)

        a[n - 1] = -1 / h
        b[n - 1] = 1 / h
        c[n - 1] = 0
        d[n - 1] = term2(time)
        Y = solve(a, b, c, d, n)
        for i in range(n):
            u[k + 1][i] = Y[i]
        time += tay


'''def expl_impl_fin_dif_scheme_appr1(u, tay, h, m, n):
    time = 0
    for i in range(1, m):
        for j in range(1, n - 1):
            u[i][j] = tay * (u[i - 1][j + 1] - 2 * u[i - 1][j] + u[i - 1][j - 1]) / h ** 2 + \
                      u[i - 1][j] + tay * additional_member(time, h * j)
        u[i][n - 1] = (term2(time) + 1 / h * u[i][n - 2] + h / (2 * tay) * u[i - 1][n - 1]) / (1 / h + h / (2 * tay))
        time += tay'''


def expl_impl_fin_dif_scheme_appr2(u, tay, h, m, n, par_a):
    time = 0
    for k in range(m - 1):
        a = np.empty(n)
        b = np.empty(n)
        c = np.empty(n)
        d = np.empty(n)
        sigma = (par_a ** 2 * tay) / (h ** 2)

        a[0] = 0
        b[0] = -(1 + sigma)
        c[0] = sigma / 2
        d[0] = -(sigma / 2 * term1(k * tay) + (1 - sigma) * u[k][0] + sigma / 2 * u[k][1]) - \
               tay * additional_member(time, 0 * h) - 0.5 * sigma * term1((k + 1) * tay)
        for j in range(1, n-1):
            a[j] = sigma / 2
            b[j] = -(1 + sigma)
            c[j] = sigma / 2
            d[j] = -(sigma / 2 * u[k][j - 1] + (1 - sigma) * u[k][j] + sigma / 2 * u[k][j + 1])\
                   - tay * additional_member(time, j * h)
        '''a[n - 1] = a[n - 2] * ((-1 / (2 * h)) / a[n - 2]) + 1 / (2 * h)
        b[n - 1] = b[n - 2] * ((-1 / (2 * h)) / a[n - 2]) - 4 / (2 * h)
        c[n - 1] = c[n - 2] * ((-1 / (2 * h)) / a[n - 2]) + 3 / (2 * h)
        d[n - 1] = d[n - 2] * ((-1 / (2 * h)) / a[n - 2]) + term2(time)'''
        # print('d:', d[n-1])
        coef = (-1 / (2 * h)) / a[n-2]
        abcd = np.array([a[n-2] * coef + 1 / (2 * h), b[n-2] * coef - 4 / (2 * h), c[n-2] * coef + 3 / (2 * h),
                         d[n-2] * coef + term2(time)])
        c[n - 1] = abcd[0]
        a[n - 1] = abcd[1]
        b[n - 1] = abcd[2]
        d[n - 1] = abcd[3]
        Y = solve(a, b, c, d, n)
        for i in range(n):
            u[k + 1][i] = Y[i]
        time += tay


def expl_impl_fin_dif_scheme_appr3(u, tay, h, m, n, par_a):
    time = 0
    for k in range(m - 1):
        a = np.empty(n)
        b = np.empty(n)
        c = np.empty(n)
        d = np.empty(n)
        sigma = (par_a ** 2 * tay) / (h ** 2)

        a[0] = 0
        b[0] = -(1 + sigma)
        c[0] = sigma / 2
        d[0] = -(sigma / 2 * term1(k * tay) + (1 - sigma) * u[k][0] + sigma / 2 * u[k][1]) - \
               tay * additional_member(time, 0 * h) - 0.5 * sigma * term1((k + 1) * tay)
        for j in range(1, n - 1):
            a[j] = sigma / 2
            b[j] = -(1 + sigma)
            c[j] = sigma / 2
            d[j] = -(sigma / 2 * u[k][j - 1] + (1 - sigma) * u[k][j] + sigma / 2 * u[k][j + 1]) \
                   - tay * additional_member(time, j * h)
        a[n - 1] = -1 / h
        b[n - 1] = (1 / h + h / (2 * tay))
        c[n - 1] = 0
        d[n - 1] = term2(time) + additional_member(time, (n - 1) * h) / h + h / (2 * tay) * u[k, n - 1]
        '''a[n - 1] = -2 / h
        b[n - 1] = 2 / h + h / tay
        c[n - 1] = 0
        d[n - 1] = h / tay * u[n - 2][n - 1] + 2 * term2((k + 1) * tay)'''

        '''print("Условие устойчивости")
        for i in range(n):
            print(a[i] + c[i] < b[i])
        print('-'*50)'''
        Y = solve(a, b, c, d, n)
        for i in range(n):
            u[k + 1][i] = Y[i]
        time += tay

'''
X = np.arange(x0, xl+h, h, dtype=np.float_)
Y = f(X, 2)
plt.plot(X, Y)
plt.plot(X, u[m-1])
plt.show()
'''