import telebot
import requests
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import os
from telebot import types

data_storage = {}
bot = telebot.TeleBot('6437147798:AAGJ2lX2LdSZkYC35WX__96SgwcTTKscuxU')

class BotState:
    def __init__(self):
        self.file_sent = False

    def set_file_sent(self, value):
        self.file_sent = value

    def get_file_sent(self):
        return self.file_sent

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
        yi_pred = model.predict(X)
        SST = np.sum((self.yi - np.mean(self.yi))**2)
        SSE = np.sum((self.yi - yi_pred)**2)
        R2 = 1 - (SSE / SST)
        R2 = round(R2, 4)
        return R2

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
            ak = np.round(ak, 4)
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
        yi_pred = model.predict(X)
        SST = np.sum((self.yi - np.mean(self.yi))**2)
        SSE = np.sum((self.yi - yi_pred)**2)
        R2 = 1 - (SSE / SST)
        R2 = round(R2, 4)
        return R2

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

bot_state = BotState()
@bot.message_handler(commands=['start'])
def greet(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Калькулятор')
    button2 = types.KeyboardButton('Инструкция')
    markup.add(button1)
    markup.add(button2)
    photo_lnk = open('img/Group.png', 'rb')
    caption = 'Привет! Я ваш новый помощник в мире статистики и машинного обучения. Я умею выполнять множественную линейную регрессию, а также помочь вам с другими задачами. Как я могу помочь вам сегодня? \n \nНажмите кнопку "Инструкция" чтобы научиться пользоваться ботом и командами'
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
        photo_lnk = open('img/lol.png', 'rb')
        file1 = open('files/Тест.txt', 'rb')
        file2 = open('files/test.txt', 'rb')
        bot.send_photo(message.chat.id, photo_lnk, 'Чтобы я мог провести для вас множественную линейную регрессию, пожалуйста, выполните следующие действия: \n\n  1) Создайте текстовый файл (например, с расширением .txt) для хранения ваших данных. \n\n  2) В каждой строке файла запишите значения переменных, разделяя их пробелами (как показано на картинке). Порядок переменных должен быть следующим:\n\n y1, x1, x2, x3, x4 или y1, x1, x2, x3 \n\n  3) После получения файла я проведу множественную линейную регрессию и предоставлю вам результаты. \n\n Вот 2 примера верного оформления файла:', reply_markup=markup)
        bot.send_document(message.chat.id, file1)
        bot.send_document(message.chat.id, file2)
    
    
    elif message.text == 'Назад' or message.text == 'назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Калькулятор')
        button2 = types.KeyboardButton('Инструкция')
        markup.add(button1)
        markup.add(button2)
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
    bot_state.set_file_sent(True)
    file_info = bot.get_file(message.document.file_id)
    file_name = message.document.file_name
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format('6437147798:AAGJ2lX2LdSZkYC35WX__96SgwcTTKscuxU', file_info.file_path))
    data = file.content.decode('utf-8').splitlines()
    columns = [] 
    num_columns = 0  
    data = file.content.decode('utf-8').splitlines()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for line in data:
        elements = line.split()
        if num_columns == 0:
            num_columns = len(elements)
            columns = [[] for _ in range(num_columns)]  # Создание списка для каждого столбца
        for i, element in enumerate(elements):
            columns[i].append(int(element))

    global yi, xi1, xi2, xi3, xi4
    if num_columns == 4:
        yi = columns[0]
        xi1 = columns[1]
        xi2 = columns[2]
        xi3 = columns[3] 
        button1 = types.KeyboardButton('yi, xi1, xi2, xi3')
        markup.add(button1)
    elif num_columns == 5:
        yi = columns[0]
        xi1 = columns[1]
        xi2 = columns[2]
        xi3 = columns[3]
        xi4 = columns[4]
        button1 = types.KeyboardButton('yi, xi1, xi2, xi3')
        button2 = types.KeyboardButton('yi, xi1, xi2, xi3, xi4')
        markup.add(button1)
        markup.add(button2)

    button3 = types.KeyboardButton('Назад')
    markup.add(button3)
    bot.send_message(message.chat.id, f"Данные из файла '{file_name}' были сохранены.", reply_markup=markup)
    bot.send_message(message.chat.id, 'Выберите способ ввода данных', reply_markup=markup)

def kef_function_XI3(message):
    if bot_state.get_file_sent():
        obj = RegressionModelXI3(xi1, xi2, xi3, yi)
        det = obj.kef_det()
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
        bot.send_message(message.chat.id, f'В нашем случае коэффициенты регрессии равны: \n{coefficients} \nА уравнение регрессии: \n{uravnenie} \nКоэффициент регрессии R^2: \n{det} \nНормированные коэффициенты равны: \n{numerical_values}')
        show = obj.show()
        bot.send_message(message.chat.id, f'Следовательно, можно сделать вывод: \n{show}')
    else:
        bot.send_message(message.chat.id, 'Вы не отправили файл!')

def kef_function_XI4(message):
    if bot_state.get_file_sent():
        obj = RegressionModelXI4(xi1, xi2, xi3, xi4, yi)
        det = obj.kef_det()
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
        bot.send_message(message.chat.id, f'В нашем случае коэффициенты регрессии равны: \n{coefficients} \nА уравнение регрессии: \n{uravnenie} \nКоэффициент регрессии R^2: \n{det} \nНормированные коэффициенты равны: \n{numerical_values}')
        show = obj.show()
        bot.send_message(message.chat.id, f'Следовательно, можно сделать вывод: \n{show}')
    else:
        bot.send_message(message.chat.id, 'Вы не отправили файл!')

bot.polling()