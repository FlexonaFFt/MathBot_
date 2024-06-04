import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

yi = [6, 8, 14, 20, 26]
xi1 = [1, 2, 1, 3, 5]
xi2 = [1, 2, 0, 2, 2]
xi3 = [2, 1, 0, 1, 2]

X = np.column_stack((np.ones(len(xi1)), xi1, xi2, xi3))
model = sm.OLS(yi, X).fit()
print(model.summary())
print("Коэффициент детерминации R^2:", round(model.rsquared, 2))

print("Коэффициенты регрессии:")
params = model.params
modus = []
for el in model.params:
    print(round(el, 2))
    modus.append(round(el, 2))

print()
y_ = []
for el in range(1, 5 + 1):
    y = params[0] + params[1] * xi1[el - 1] + params[2] * xi2[el - 1] + params[3] * xi3[el - 1]
    r_y = round(y, 2)
    y_.append(r_y)
    print(r_y)

print()
y_y_ = []
for el in range(1, 6):
    rez = yi[el - 1] - y_[el - 1]
    r_rez = round(rez, 2)
    y_y_.append(r_rez)
    print(r_rez)

print()
y__y = []
for el in y_y_:
    rez = el ** 2 
    rez = round(rez, 4)
    y__y.append(rez)
    print(rez)

print()
summaru_y__y = sum(y__y)
print(summaru_y__y)

# Ищем отношение диагональных элементов
X = np.array([xi1, xi2, xi3]).T
X = sm.add_constant(X)
XtX = np.dot(X.T, X)
XtX_inv = np.linalg.inv(XtX)
diagonal = np.diagonal(XtX_inv)
print()
print(diagonal)

print()
Betta_summary = []
for el in diagonal:
    rez = summaru_y__y * el
    rez = round(rez, 2)
    Betta_summary.append(rez)
    print(rez)

print()
sqrt_betta_summary = []
for el in Betta_summary:
    rez = np.sqrt(el)
    rez = round(rez, 2)
    sqrt_betta_summary.append(rez)
    print(rez)

print()
yi = np.array([6, 8, 14, 20, 26])
yi_T = yi.reshape(5, 1)
yi_dot_yi_T = np.dot(yi, yi_T)
u_ = sum(yi) / len(yi)
u__u = u_ ** 2
si = np.sqrt((yi_dot_yi_T) / len(yi) - u__u)
for el in si:
    si = round(el, 2)
print(si)

print()
a = []
for k in range(1, 3 + 1):
    ak = modus[k] * (sqrt_betta_summary[k] / si)
    ak = round(ak, 2)
    a.append(ak)
    print(ak)