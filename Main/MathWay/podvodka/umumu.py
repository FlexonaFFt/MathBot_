import numpy as np

X = np.array([[1, 17, 130, 523, 2517], 
            [1, 22,  180, 518, 2801], 
            [1, 18,  217, 510, 2573],  
            [1, 24, 103, 516, 2643], 
            [1, 19, 171, 511, 2801], 
            [1, 20, 180, 471, 2815], 
            [1, 17,  140, 523, 2527], 
            [1, 21, 92, 498, 2735], 
            [1, 18,  173, 542, 2817], 
            [1, 22,  87, 501, 2736], 
            [1, 20,  93, 471, 2682], 
            [1, 17, 210, 523, 2593],
            [1, 15, 110, 538, 2627], 
            [1, 21, 86, 472, 2532],
            [1, 15, 175, 467, 2693]])

y = np.array([401,452,478,397,453,427,396,399,418,413,412,423,393,381,401])

beta = np.linalg.inv(X.T @ X) @ X.T @ y
beta = np.round(beta, 5)

# коэффициент детерминации R^2
y_pred = X @ beta
SSR = np.sum((y_pred - np.mean(y))**2)
SST = np.sum((y - np.mean(y))**2)
R2 = np.round(SSR / SST, 5)

# Нормированные коэффициенты
n = len(y)
m = X.shape[1] - 1
errors = y - y_pred
S2_e = np.sum(errors**2) / (n - m - 1)
X_inv = np.linalg.inv(X.T @ X)
S_beta = np.sqrt(np.diag(S2_e * X_inv))

S_y = np.sqrt((y.T @ y) / n - np.mean(y)**2)
a = np.round(beta * S_beta / S_y, 4)

print("Коэффициенты:")
print(f"β_0^* = {beta[0]} \nβ_1^* = {beta[1]} \nβ_2^* = {beta[2]} \nβ_3^* = {beta[3]} \nβ_4^* = {beta[4]}")
print()
print("Коэффициент детерминации:")
print(f"R^2 = {R2}")
print()
print("Нормированные коэффициенты:")
print(f"a_1 = {a[1]} \na_2 = {a[2]} \na_3 = {a[3]} \na_4 = {a[4]}")
print(S_beta)