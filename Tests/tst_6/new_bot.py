import numpy as np
import telebot
from telebot import types
import requests

data_storage = {}
bot = telebot.TeleBot('6437147798:AAGJ2lX2LdSZkYC35WX__96SgwcTTKscuxU')


class BotState:


    def __init__(self):
        self.file_sent = False

    def set_file_sent(self, value):
        self.file_sent = value

    def get_file_sent(self):
        return self.file_sent

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
        for i in range(5):  # Ensure we are trying to access up to the 5th coefficient
            print(f"β_{i}^* = {self.beta[i]}")
        print()
        print("Коэффициент детерминации:")
        print(f"R^2 = {self.R2}")
        print()
        print("Нормированные коэффициенты:")
        for i in range(1, 5):  # Ensure we are trying to access up to the 4th normalized coefficient
            print(f"a_{i} = {self.a[i]}")


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
        button2 = types.KeyboardButton('yi, xi1, xi2, xi3, xi4')
        button3 = types.KeyboardButton('Назад')
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
    
    elif message.text == 'yi, xi1, xi2, xi3, xi4':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Назад')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Получаем результаты: ', reply_markup=markup)
        RegressionModel(message)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    bot_state.set_file_sent(True)
    file_info = bot.get_file(message.document.file_id)
    file_name = message.document.file_name
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format('6437147798:AAGJ2lX2LdSZkYC35WX__96SgwcTTKscuxU', file_info.file_path))
    data = file.content.decode('utf-8').splitlines()
    data = file.content.decode('utf-8').splitlines()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    X = []
    Y = []

    for line in data:
        elements = line.split()
        Y.append(int(elements[0]))
        X.append([int(x) for x in elements[1:]])

    X = np.array(X)
    Y = np.array(Y)

    global yi, xi1, xi2, xi3, xi4
    model = RegressionModel(X, Y)
    model.calculate_beta()
    model.calculate_r2()
    model.calculate_normalized_coefficients()
    model.print_results()

# def kef_function_XI3(message):
#     if bot_state.get_file_sent():
#         model = RegressionModel(X, y)
#         model.calculate_beta()
#         model.calculate_r2()
#         model.calculate_normalized_coefficients()
#         model.print_results()
#         bot.send_message()
#     else:
#         bot.send_message(message.chat.id, 'Вы не отправили файл!')

bot.polling()