# Подключение необходимых библиотек
import numpy as np
import matplotlib.pyplot as plt

# Введение необходимых переменных
xi = [3.4, 3.8, 4.0, 3.0, 3.7, 3.0, 3.5, 3.8, 3.1, 3.0]
yi = [3.5, 3.8, 3.9, 3.3, 3.7, 3.4, 3.6, 4.0, 3.4, 3.1]
xixi = []
xiyi = []
yiyi = []

sumxi = sumyi = sumxixi = sumxiyi = sumyiyi= 0

# Расчёт дополнительных переменных
for element in range(len(xi)):
    xixi.append(round(xi[element] * xi[element], 2))
    xiyi.append(round(xi[element] * yi[element], 2))
    yiyi.append(round(yi[element] * yi[element], 2))

# Расчёт значений сумм всех переменных
sumxi = sum(xi)
sumyi = sum(yi)
sumxixi = sum(xixi)
sumxiyi = sum(xiyi)
sumyiyi = sum(yiyi)

# решим систему уравнений
# Создаем матрицу коэффициентов и вектор свободных членов
A = np.array([[sumxi, len(xi)], [sumxixi, sumxi]])
b = np.array([sumyi, sumxiyi])

# Решаем систему уравнений
x = np.linalg.solve(A, b)

# Выводим промежуточный результат
print('Следовательно, зависимость будет выражаться следующим уравнением: ')
print(f'вектор yx = {x[0]:.2f}x + {x[1]:.2f}')

print('Далее идёт вычисление коэффициента корреляции.')
qus_ = input("Хотите предварительно построить график линейной регрессии? (Y/N): ")

if qus_ == 'Y':
    a = round(x[0], 2)
    b = round(x[1], 2)
    # Программная запись уравнения линейной регрессии
    def linear_regression(x):
        return a * x + b

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

    elements_cnt = len(xi)
    # Вычисляем коэффициент корреляции
    qx = np.sqrt(sumxixi / elements_cnt - (sumxi / elements_cnt) ** 2)
    qy = np.sqrt(sumyiyi / elements_cnt - (sumyi / elements_cnt) ** 2)

    r = (sumxiyi / elements_cnt - (sumxi / elements_cnt) * (sumyi / elements_cnt)) / (qx * qy)

    # Выводим коэффициент корреляции
    print(f'Коэффициент корреляции: {r:.2f}')

elif qus_ == 'N':
    elements_cnt = len(xi)
    # Вычисляем коэффициент корреляции
    qx = np.sqrt(sumxixi / elements_cnt - (sumxi / elements_cnt) ** 2)
    qy = np.sqrt(sumyiyi / elements_cnt - (sumyi / elements_cnt) ** 2)

    r = (sumxiyi / elements_cnt - (sumxi / elements_cnt) * (sumyi / elements_cnt)) / (qx * qy)

    # Выводим коэффициент корреляции
    print(f'Коэффициент корреляции: {r:.2f}')