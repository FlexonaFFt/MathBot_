# Подключение необходимых библиотек
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=2)

# Введение необходимых переменных
xi = [3.4, 3.8, 4.0, 3.0, 3.7, 3.0, 3.5, 3.8, 3.1, 3.0]
yi = [3.5, 3.8, 3.9, 3.3, 3.7, 3.4, 3.6, 4.0, 3.4, 3.1]

# Создание матриц x и y
x = np.zeros((len(xi), 2))
x[:, 0] = 1
x[:, 1] = xi
x_t = x.T
y = np.array(yi).reshape(-1, 1)

# Вычисление произведения транспонированной матрицы на обычную
product = x_t @ x
# Нахождение обратной матрицы
product_inv = np.linalg.inv(product)
# Нахождения результата
result = product_inv @ x_t @ y

# Запись уравнения линейной регрессии
a = result[0][0]
b = result[1][0]
print(f'y = {b:.2f}x + {a:.2f}')

qus_ = input("Хотите построить график линейной регрессии? (Y/N): ")

if qus_ == 'Y':
    # Программная запись уравнения линейной регрессии
    def linear_regression(x):
        return b * x + a

    x_values = np.array([3.4, 3.8, 4.0, 3.0, 3.7, 3.0, 3.5, 3.8, 3.1, 3.0])
    y_values = linear_regression(x_values)

    # Построение графика
    plt.scatter(x_values, y_values, color='blue', label='Исходные данные')
    plt.plot(x_values, linear_regression(x_values), color='red', label='Линейная регрессия')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('График линейной регрессии')
    plt.legend()
    plt.grid(True)
    plt.show()

elif qus_ == 'N':
    print('Программа завершена')