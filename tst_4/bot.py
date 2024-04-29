import telebot
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import os
from telebot import types

data_storage = {}
bot = telebot.TeleBot('6437147798:AAGJ2lX2LdSZkYC35WX__96SgwcTTKscuxU')
yi = [401, 452, 478, 397, 453, 427, 396, 399, 418, 413, 412, 423, 393, 381, 401]
xi1 = [17, 22, 18, 24, 19, 20, 17, 21, 18, 22, 20, 17, 15, 21, 15]
xi2 = [130, 180, 217, 103, 171, 180, 140, 92, 173, 87, 93, 210, 110, 86, 175]
xi3 = [523, 518, 510, 516, 511, 471, 523, 498, 542, 501, 471, 523, 538, 472, 467]
xi4 = [2517, 2801, 2573, 2643, 2801, 2815, 2527, 2735, 2817, 2736, 2682, 2593, 2627, 2532, 2693]

yi_ = [6, 8, 14, 20, 26]
xi1_ = [1, 2, 1, 3, 5]
xi2_ = [1, 2, 0, 2, 2]
xi3_ = [2, 1, 0, 1, 2]

class RegressionModelXI4:
    def __init__(self, xi1, xi2, xi3, xi4, yi):
        self.xi1 = xi1
        self.xi2 = xi2
        self.xi3 = xi3
        self.xi4 = xi4
        self.yi = yi
        self.n = len(self.yi)

    # Коэффициент детерминации
    def kef_det(self):
        X = np.column_stack((np.ones(len(self.xi1)), self.xi1, self.xi2, self.xi3, self.xi4))
        model = sm.OLS(self.yi, X).fit()
        return model.summary()

    # Коэффициенты регрессии
    def kef_reg(self):
        X = np.column_stack((np.ones(len(self.xi1)), self.xi1, self.xi2, self.xi3, self.xi4))
        model = sm.OLS(self.yi, X).fit()
        self.params = model.params
        self.modus = []
        for el in model.params:
            self.modus.append(round(el, 2))
        return self.modus
    
    # Составление уравнения регрессии
    def regression_equation(self):
        Y = f'{round(self.params[0], 2)} + {round(self.params[1], 2)}xi1 + {round(self.params[2], 2)}xi2 + {round(self.params[3], 2)}xi3 + {round(self.params[4], 2)}xi4'
        return Y
    
    # Нахождение нормированных коэффициентов
    # Нахождение значений уравнений при заданных xi1, xi2, xi3, xi4
    def kef_y_(self):
        self.y_ = []
        for el in range(1, self.n + 1):
            y = self.params[0] + self.params[1] * self.xi1[el - 1] + self.params[2] * self.xi2[el - 1] + self.params[3] * self.xi3[el - 1] + self.params[4] * self.xi3[el - 1]
            r_y = round(y, 2)
            self.y_.append(r_y)
        return self.y_
        
    # Нахождение разности yi-yi*
    def kef_y_yi(self):
        self.y_y_ = []
        for el in range(1, self.n + 1):
            rez = self.yi[el - 1] - self.y_[el - 1]
            r_rez = round(rez, 2)
            self.y_y_.append(r_rez)
        return self.y_y_
    
    # Нахождение квадрата разности yi-yi*
    def kef_y__y(self):
        self.y__y = []
        for el in self.y_y_:
            rez = el ** 2 
            rez = round(rez, 4)
            self.y__y.append(rez)
        return self.y__y
    
    # Нахождение итоговой суммы y__y:
    def kef_summary__y__y(self):
        self.summary_y__y = sum(self.y__y)
        return self.summary_y__y
    
    # Нахождение отношения диагональных элементов
    def kef_diagonal(self):
        X = np.array([self.xi1, self.xi2, self.xi3, self.xi4]).T
        X = sm.add_constant(X)
        XtX = np.dot(X.T, X)
        XtX_inv = np.linalg.inv(XtX)
        self.diagonal = np.diagonal(XtX_inv)
        return self.diagonal
    
    # Нахождение суммаризации диагональных элементов и итоговой суммы
    def kef_betta_summary(self):
        self.diagonal = self.kef_diagonal()
        self.Betta_summary = []
        for el in self.diagonal:
            rez = self.kef_summary__y__y() * el
            rez = round(rez, 2)
            self.Betta_summary.append(rez)
        return self.Betta_summary
    
    # Нахождения подкоренного выражения представленной формулы
    def kef_sqrt_b_summ(self):
        sqrt_betta_summary = []
        for el in self.Betta_summary:
            rez = np.sqrt(el)
            rez = round(rez, 2)
            sqrt_betta_summary.append(rez)
        return sqrt_betta_summary
    
    # Нахождения Si
    def kef_si(self):
        yi = np.array(self.yi)
        yi_T = yi.reshape(len(self.yi), 1)
        yi_dot_yi_T = np.dot(yi, yi_T)
        u_ = sum(yi) / len(yi)
        u__u = u_ ** 2
        self.dot = np.sqrt((yi_dot_yi_T) / len(yi) - u__u)
        self.si = np.round(self.dot, 2)
        return self.si

    # Непосредственно нахождение коэффициентов
    def kef_coef(self):
        self.a = []
        self.modus = self.kef_reg()
        self.Betta_summary = self.kef_sqrt_b_summ()
        for k in range(1, 4 + 1):
            ak = self.modus[k] * (self.Betta_summary[k] / self.si)
            ak = np.round(ak, 2)
            self.a.append(ak)
        return self.a
    
    # Выводим численное представление ответа
    def print_numerical_values(self):
        slov = []
        numerical_values = [item[0] for item in self.a]
        for value in numerical_values:
            slov.append(value)
        return slov 
    
    # Вывод
    def show(self):
        if abs(self.a[0]) > abs(self.a[1]) and abs(self.a[0]) > abs(self.a[2]) and abs(self.a[0]) > abs(self.a[3]):
            return f'Итак, для переменной xi1 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi2, xi3, xi4'
        elif abs(self.a[1]) > abs(self.a[0]) and abs(self.a[1]) > abs(self.a[2]) and abs(self.a[1]) > abs(self.a[3]):
            return f'Итак, для переменной xi2 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi3, xi4'
        elif abs(self.a[2]) > abs(self.a[0]) and abs(self.a[2]) > abs(self.a[1]) and abs(self.a[2]) > abs(self.a[3]):
            return f'Итак, для переменной xi3 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi2, xi4'
        elif abs(self.a[3]) > abs(self.a[0]) and abs(self.a[3]) > abs(self.a[1]) and abs(self.a[3]) > abs(self.a[2]):
            return f'Итак, для переменной xi4 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi2, xi3'


class RegressionModelXI3:
    def __init__(self, xi1, xi2, xi3, yi):
        self.xi1 = xi1
        self.xi2 = xi2
        self.xi3 = xi3
        self.yi = yi
        self.n = len(self.yi)

    # Коэффициент детерминации
    def kef_det(self):
        X = np.column_stack((np.ones(len(self.xi1)), self.xi1, self.xi2, self.xi3))
        model = sm.OLS(self.yi, X).fit()
        return model.summary()

    # Коэффициенты регрессии
    def kef_reg(self):
        X = np.column_stack((np.ones(len(self.xi1)), self.xi1, self.xi2, self.xi3))
        model = sm.OLS(self.yi, X).fit()
        self.params = model.params
        self.modus = []
        for el in model.params:
            self.modus.append(round(el, 2))
        return self.modus
    
    # Составление уравнения регрессии
    def regression_equation(self):
        Y = f'{round(self.params[0], 2)} + {round(self.params[1], 2)}xi1 + {round(self.params[2], 2)}xi2 + {round(self.params[3], 2)}xi3'
        return Y
    
    # Нахождение нормированных коэффициентов
    # Нахождение значений уравнений при заданных xi1, xi2, xi3, xi4
    def kef_y_(self):
        self.y_ = []
        for el in range(1, self.n + 1):
            y = self.params[0] + self.params[1] * self.xi1[el - 1] + self.params[2] * self.xi2[el - 1] + self.params[3] * self.xi3[el - 1]
            r_y = round(y, 2)
            self.y_.append(r_y)
        return self.y_
        
    # Нахождение разности yi-yi*
    def kef_y_yi(self):
        self.y_y_ = []
        for el in range(1, self.n + 1):
            rez = self.yi[el - 1] - self.y_[el - 1]
            r_rez = round(rez, 2)
            self.y_y_.append(r_rez)
        return self.y_y_
    
    # Нахождение квадрата разности yi-yi*
    def kef_y__y(self):
        self.y__y = []
        for el in self.y_y_:
            rez = el ** 2 
            rez = round(rez, 4)
            self.y__y.append(rez)
        return self.y__y
    
    # Нахождение итоговой суммы y__y:
    def kef_summary__y__y(self):
        self.summary_y__y = sum(self.y__y)
        return self.summary_y__y
    
    # Нахождение отношения диагональных элементов
    def kef_diagonal(self):
        X = np.array([self.xi1, self.xi2, self.xi3]).T
        X = sm.add_constant(X)
        XtX = np.dot(X.T, X)
        XtX_inv = np.linalg.inv(XtX)
        self.diagonal = np.diagonal(XtX_inv)
        return self.diagonal
    
    # Нахождение суммаризации диагональных элементов и итоговой суммы
    def kef_betta_summary(self):
        self.diagonal = self.kef_diagonal()
        self.Betta_summary = []
        for el in self.diagonal:
            rez = self.kef_summary__y__y() * el
            rez = round(rez, 2)
            self.Betta_summary.append(rez)
        return self.Betta_summary
    
    # Нахождения подкоренного выражения представленной формулы
    def kef_sqrt_b_summ(self):
        sqrt_betta_summary = []
        for el in self.Betta_summary:
            rez = np.sqrt(el)
            rez = round(rez, 2)
            sqrt_betta_summary.append(rez)
        return sqrt_betta_summary
    
    # Нахождения Si
    def kef_si(self):
        yi = np.array(self.yi)
        yi_T = yi.reshape(len(self.yi), 1)
        yi_dot_yi_T = np.dot(yi, yi_T)
        u_ = sum(yi) / len(yi)
        u__u = u_ ** 2
        self.dot = np.sqrt((yi_dot_yi_T) / len(yi) - u__u)
        self.si = np.round(self.dot, 2)
        return self.si

    # Непосредственно нахождение коэффициентов
    def kef_coef(self):
        self.a = []
        self.modus = self.kef_reg()
        self.Betta_summary = self.kef_sqrt_b_summ()
        for k in range(1, 3 + 1):
            ak = self.modus[k] * (self.Betta_summary[k] / self.si)
            ak = np.round(ak, 2)
            self.a.append(ak)
        return self.a
    
    # Выводим численное представление ответа
    def print_numerical_values(self):
        slov = []
        numerical_values = [item[0] for item in self.a]
        for value in numerical_values:
            slov.append(value)
        return slov 
    
    # Вывод
    def show(self):
        if abs(self.a[0]) > abs(self.a[1]) and abs(self.a[0]) > abs(self.a[2]):
            return f'Для переменной xi1 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi2, xi3'
        elif abs(self.a[1]) > abs(self.a[0]) and abs(self.a[1]) > abs(self.a[2]):
            return f'Для переменной xi2 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi3'
        elif abs(self.a[2]) > abs(self.a[0]) and abs(self.a[2]) > abs(self.a[1]):
            return f'Для переменной xi3 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi2'

@bot.message_handler(commands=['start'])
def greet(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Калькулятор')
    button2 = types.KeyboardButton('Инструкция')
    button3 = types.KeyboardButton('О боте')
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    photo_lnk = open('img/tst.jpg', 'rb')
    caption = 'Привет! Я ваш новый помощник в мире статистики и машинного обучения. Я умею выполнять множественную линейную регрессию, а также помочь вам с другими задачами. Как я могу помочь вам сегодня?'
    bot.send_photo(message.chat.id, photo_lnk, caption, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Калькулятор' or message.text == 'калькулятор':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('yi, xi1, xi2, xi3')
        button2 = types.KeyboardButton('yi, xi1, xi2, xi3, xi4')
        button3 = types.KeyboardButton('Назад')
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        bot.send_message(message.chat.id, 'Выберите способ ввода данных', reply_markup=markup)
    
    elif message.text == 'Инструкция' or message.text == 'инструкция':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Назад')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Инструкция', reply_markup=markup)
    
    elif message.text == 'О боте' or message.text == 'о боте':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Назад')
        markup.add(button1)
        bot.send_message(message.chat.id, 'О боте', reply_markup=markup)
    
    elif message.text == 'Назад' or message.text == 'назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Калькулятор')
        button2 = types.KeyboardButton('Инструкция')
        button3 = types.KeyboardButton('О боте')
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        bot.send_message(message.chat.id, 'Выберите способ ввода данных', reply_markup=markup)

    elif message.text == 'yi, xi1, xi2, xi3':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Назад')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Получаем результаты: ', reply_markup=markup)
        kef_function_XI3(message)
    
    elif message.text == 'yi, xi1, xi2, xi3, xi4':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Назад')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Получаем результаты: ', reply_markup=markup)
        kef_function_XI4(message)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    file_name = message.document.file_name
    file_path = os.path.join('files', file_name)
    
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        columns = []
        for line in lines:
            data = line.strip().split()
            for i, value in enumerate(data):
                if len(columns) <= i:
                    columns.append([])
                columns[i].append(value)
    
    data_storage[file_name] = columns

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('yi, xi1, xi2, xi3')
    button2 = types.KeyboardButton('yi, xi1, xi2, xi3, xi4')
    button3 = types.KeyboardButton('Назад')
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, 'Выберите способ ввода данных', reply_markup=markup)
    bot.send_message(message.chat.id, f"Данные из файла '{file_name}' были сохранены.", reply_markup=markup)

def kef_function_XI3(message):
    obj = RegressionModelXI3(xi1_, xi2_, xi3_, yi_)
    coefficients = obj.kef_reg()
    uravnenie = obj.regression_equation()
    obj.kef_y_()
    obj.kef_y_yi()
    obj.kef_y__y()
    obj.kef_diagonal()
    obj.kef_betta_summary()
    obj.kef_sqrt_b_summ()
    obj.kef_si()
    obj.kef_coef()
    numerical_values = obj.print_numerical_values()
    bot.send_message(message.chat.id, f'В нашем случае коэффициенты регрессии равны: \n{coefficients} \nА уравнение регрессии: \n{uravnenie} \nНормированные коэффициенты равны: \n{numerical_values}')
    show = obj.show()
    bot.send_message(message.chat.id, f'Следовательно, можно сделать вывод: \n{show}')

def kef_function_XI4(message):
    obj = RegressionModelXI4(xi1, xi2, xi3, xi4, yi)
    coefficients = obj.kef_reg()
    uravnenie = obj.regression_equation()
    obj.kef_y_()
    obj.kef_y_yi()
    obj.kef_y__y()
    obj.kef_diagonal()
    obj.kef_betta_summary()
    obj.kef_sqrt_b_summ()
    obj.kef_si()
    obj.kef_coef()
    numerical_values = obj.print_numerical_values()
    bot.send_message(message.chat.id, f'В нашем случае коэффициенты регрессии равны: \n{coefficients} \nА уравнение регрессии: \n{uravnenie} \nНормированные коэффициенты равны: \n{numerical_values}')
    show = obj.show()
    bot.send_message(message.chat.id, f'Следовательно, можно сделать вывод: \n{show}')

bot.polling()