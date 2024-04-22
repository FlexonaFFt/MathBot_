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
print("Коэффициент детерминации R^2:", model.rsquared)

print("Коэффициенты регрессии:")
params = model.params
print(model.params)

rse = np.sqrt(model.mse_resid)
print("Среднеквадратичное отклонение случайного фактора:", rse)