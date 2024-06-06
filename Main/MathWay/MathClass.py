import numpy as np

class RegressionModel:
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def calculate_beta(self):
        self.beta = np.linalg.inv(self.X.T @ self.X) @ self.X.T @ self.y
        self.beta = np.round(self.beta, 5)
        return self.beta

    def calculate_r2(self):
        self.y_pred = self.X @ self.beta
        self.SSR = np.sum((self.y_pred - np.mean(self.y)) ** 2)
        self.SST = np.sum((self.y - np.mean(self.y)) ** 2)
        self.R2 = np.round(self.SSR / self.SST, 5)
        return self.R2

    def calculate_normalized_coefficients(self):
        self.n = len(self.y)
        self.m = self.X.shape[1] - 1
        self.errors = self.y - self.y_pred
        self.S2_e = np.sum(self.errors ** 2) / (self.n - self.m - 1)
        self.X_inv = np.linalg.inv(self.X.T @ self.X)
        self.S_beta = np.sqrt(np.diag(self.S2_e * self.X_inv))
        self.S_y = np.sqrt((self.y.T @ self.y) / self.n - np.mean(self.y) ** 2)
        self.a = np.round(self.beta * self.S_beta / self.S_y, 4)
        return self.a

    def print_results(self):
        print("Коэффициенты:")
        print(f"β_0^* = {self.beta[0]} \nβ_1^* = {self.beta[1]} \nβ_2^* = {self.beta[2]} \nβ_3^* = {self.beta[3]} \nβ_4^* = {self.beta[4]}")
        print()
        print("Коэффициент детерминации:")
        print(f"R^2 = {self.R2}")
        print()
        print("Нормированные коэффициенты:")
        print(f"a_1 = {self.a[1]} \na_2 = {self.a[2]} \na_3 = {self.a[3]} \na_4 = {self.a[4]}")
        print()
        result = ''
        if abs(self.a[0]) > abs(self.a[1]) and abs(self.a[0]) > abs(self.a[2]):
            result += f'\nДля переменной xi1 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi2, xi3'
        elif abs(self.a[1]) > abs(self.a[0]) and abs(self.a[1]) > abs(self.a[2]):
            result += f'\nДля переменной xi2 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi3'
        elif abs(self.a[2]) > abs(self.a[0]) and abs(self.a[2]) > abs(self.a[1]):
            result += f'\nДля переменной xi3 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi2'
        print(result)


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


model = RegressionModel(X, y)
model.calculate_beta()
model.calculate_r2()
model.calculate_normalized_coefficients()
model.print_results()