import telebot
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import os
from telebot import types

bot = telebot.TeleBot('6437147798:AAGJ2lX2LdSZkYC35WX__96SgwcTTKscuxU')

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
        bot.send_message(message.chat.id, 'Отправьте файл xlsx файл с данными', reply_markup=markup)

@bot.message_handler(content_types=['document'])
async def handle_document(message):
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    try:
        with open("downloaded_file.xlsx", "wb") as f:
            f.write(downloaded_file)
        df = pd.read_excel("downloaded_file.xlsx")
        await bot.send_message(chat_id=message.chat.id, text="Файл успешно загружен и проверен!")
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text=f"Произошла ошибка при обработке файла: {str(e)}")
    finally:
        os.remove("downloaded_file.xlsx")

def kef_function_XI3(message):
    obj = RegressionModelXI3()


bot.polling()

class RegressionModelXI4:
    def __init__(self, file_path):
        self.file_path = file_path
        self.read_data()

    def read_data(self):
        df = pd.read_excel(self.file_path)
        self.yi = df.iloc[:, 0].values
        self.xi1 = df.iloc[:, 1].values
        self.xi2 = df.iloc[:, 2].values
        self.xi3 = df.iloc[:, 3].values
        self.xi4 = df.iloc[:, 4].values
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
        modus = []
        for el in model.params:
            modus.append(round(el, 2))
        return modus
    
    # Составление уравнения регрессии
    def regression_equation(self):
        Y = f'{self.params[0]} + {self.params[1]}xi1 + {self.params[2]}xi2 + {self.params[3]}xi3 + {self.params[4]}xi4'
        return Y
    
    # Нахождение нормированных коэффициентов
    # Нахождение значений уравнений при заданных xi1, xi2, xi3, xi4
    def kef_y_(self):
        self.y_ = []
        for el in range(1, self.n + 1):
            y = self.params[0] + self.params[1] * self.xi1[el - 1] + self.params[2] * self.xi2[el - 1] + self.params[3] * self.xi3[el - 1] + self.params[4] * self.xi4[el - 1]
            r_y = round(y, 2)
            self.y_.append(r_y)
        return self.y_
        
    # Нахождение разности yi-yi*
    def kef_y_yi(self):
        self.y_y_ = []
        for el in range(1, self.n):
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
        self.summaru_y__y = sum(self.y__y)
        return self.summaru_y__y
    
    # Нахождение отношения диагональных элементов
    def kef_diagonal(self):
        X = np.array([self.xi1, self.xi2, self.xi3, self.xi4]).T
        X = sm.add_constant(X)
        XtX = np.dot(X.T, X)
        XtX_inv = np.linalg.inv(XtX)
        diagonal_ = np.diagonal(XtX_inv)
        return diagonal_
    
    # Нахождение суммаризации диагональных элементов и итоговой суммы
    def kef_betta_summary(self):
        self.Betta_summary = []
        for el in self.diagonal:
            rez = self.summaru_y__y * el
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
        self.si = np.sqrt((yi_dot_yi_T) / len(yi) - u__u)
        for el in self.si:
            self.si = round(el, 2)

    # Непосредственно нахождение коэффициентов
    def kef_coef(self):
        a = []
        for k in range(1, 4 + 1):
            ak = self.modus[k] * (self.sqrt_betta_summary[k] / self.si)
            ak = round(ak, 2)
            a.append(ak)
        return self.a
    
    # Вывод
    def show(self):
        if abs(self.a[0]) > abs(self.a[1]) and abs(self.a[0]) > abs(self.a[2]) and abs(self.a[0]) > abs(self.a[3]):
            print('Итак, для переменной xi1 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi2, xi3, xi4')
        elif abs(self.a[1]) > abs(self.a[0]) and abs(self.a[1]) > abs(self.a[2]) and abs(self.a[1]) > abs(self.a[3]):
            print('Итак, для переменной xi2 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi3, xi4')
        elif abs(self.a[2]) > abs(self.a[0]) and abs(self.a[2]) > abs(self.a[1]) and abs(self.a[2]) > abs(self.a[3]):
            print('Итак, для переменной xi3 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi2, xi4')
        elif abs(self.a[3]) > abs(self.a[0]) and abs(self.a[3]) > abs(self.a[1]) and abs(self.a[3]) > abs(self.a[2]):
            print('Итак, для переменной xi4 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi2, xi3')
                                

class RegressionModelXI3:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_data()
        self.yi = self.data['yi']
        self.xi1 = self.data['xi1']
        self.xi2 = self.data['xi2']
        self.xi3 = self.data['xi3']
    
    def read_data(self):
        data = pd.read_csv(self.file_path, sep='\t', header=None, names=['yi', 'xi1', 'xi2', 'xi3'])
        return data

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
        modus = []
        for el in model.params:
            modus.append(round(el, 2))
        return modus
    
    # Составление уравнения регрессии
    def regression_equation(self):
        Y = f'{self.params[0]} + {self.params[1]}xi1 + {self.params[2]}xi2 + {self.params[3]}xi3'
        return Y
    
    # Нахождение нормированных коэффициентов
    # Нахождение значений уравнений при заданных xi1, xi2, xi3
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
        for el in range(1, self.n):
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
        self.summaru_y__y = sum(self.y__y)
        return self.summaru_y__y
    
    # Нахождение отношения диагональных элементов
    def kef_diagonal(self):
        X = np.array([self.xi1, self.xi2, self.xi3]).T
        X = sm.add_constant(X)
        XtX = np.dot(X.T, X)
        XtX_inv = np.linalg.inv(XtX)
        diagonal_ = np.diagonal(XtX_inv)
        return diagonal_
    
    # Нахождение суммаризации диагональных элементов и итоговой суммы
    def kef_betta_summary(self):
        self.Betta_summary = []
        for el in self.diagonal:
            rez = self.summaru_y__y * el
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
        self.si = np.sqrt((yi_dot_yi_T) / len(yi) - u__u)
        for el in self.si:
            self.si = round(el, 2)

    # Непосредственно нахождение коэффициентов
    def kef_coef(self):
        a = []
        for k in range(1, 3 + 1):
            ak = self.modus[k] * (self.sqrt_betta_summary[k] / self.si)
            ak = round(ak, 2)
            a.append(ak)
        return self.a
    
    # Вывод
    def show(self):
        if abs(self.a[0]) > abs(self.a[1]) and abs(self.a[0]) > abs(self.a[2]):
            print('Итак, для переменной xi1 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi2, xi3')
        elif abs(self.a[1]) > abs(self.a[0]) and abs(self.a[1]) > abs(self.a[2]):
            print('Итак, для переменной xi2 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi3')
        elif abs(self.a[2]) > abs(self.a[0]) and abs(self.a[2]) > abs(self.a[1]):
            print('Итак, для переменной xi3 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi2')