import telebot
import os
import numpy as np
from telebot import types

API_TOKEN = '6437147798:AAGJ2lX2LdSZkYC35WX__96SgwcTTKscuxU'
bot = telebot.TeleBot(API_TOKEN)

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

    def get_results(self):
        result = "Коэффициенты:\n"
        result += f"β_0^* = {self.beta[0]} \nβ_1^* = {self.beta[1]} \nβ_2^* = {self.beta[2]} \nβ_3^* = {self.beta[3]} \nβ_4^* = {self.beta[4]}\n\n"
        result += "Коэффициент детерминации:\n"
        result += f"R^2 = {self.R2}\n\n"
        result += "Нормированные коэффициенты:\n"
        result += f"a_1 = {self.a[1]} \na_2 = {self.a[2]} \na_3 = {self.a[3]} \na_4 = {self.a[4]}\n"
        if abs(self.a[0]) > abs(self.a[1]) and abs(self.a[0]) > abs(self.a[2]):
            result += f'\nДля переменной xi1 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi2, xi3'
        elif abs(self.a[1]) > abs(self.a[0]) and abs(self.a[1]) > abs(self.a[2]):
            result += f'\nДля переменной xi2 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi3'
        elif abs(self.a[2]) > abs(self.a[0]) and abs(self.a[2]) > abs(self.a[1]):
            result += f'\nДля переменной xi3 влияние на признак Y является наиболее эффективным в сравнении с действием переменных xi1, xi2'
        return result

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Инструкция')
    markup.add(button)
    bot.send_message(message.chat.id, 'Привет! Я ваш новый помощник в мире статистики и машинного обучения. Я умею выполнять множественную линейную регрессию, а также помочь вам с другими задачами. Как я могу помочь вам сегодня? \n \nНажмите кнопку "Инструкция" чтобы научиться пользоваться ботом и командами.')
    bot.reply_to(message, "Дли анализа отправь мне текстовый файл, и я обработаю его.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
        message.text == 'Инструкция' or message.text == 'инструкция'
        photo_lnk = open('img/lol.png', 'rb')
        file1 = open('files/Тест.txt', 'rb')
        file2 = open('files/test.txt', 'rb')
        bot.send_photo(message.chat.id, photo_lnk, 'Чтобы я мог провести для вас множественную линейную регрессию, пожалуйста, выполните следующие действия: \n\n  1) Создайте текстовый файл (например, с расширением .txt) для хранения ваших данных. \n\n  2) В каждой строке файла запишите значения переменных, разделяя их пробелами (как показано на картинке). Порядок переменных должен быть следующим:\n\n y1, x1, x2, x3, x4 или y1, x1, x2, x3 \n\n  3) После получения файла я проведу множественную линейную регрессию и предоставлю вам результаты. \n\n Вот 2 примера верного оформления файла:')
        bot.send_document(message.chat.id, file1)
        bot.send_document(message.chat.id, file2)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("received_file.txt", 'wb') as new_file:
            new_file.write(downloaded_file)

        # Обработка файла
        data = np.loadtxt("received_file.txt")
        X = np.hstack((np.ones((data.shape[0], 1)), data[:, 1:]))
        y = data[:, 0]

        model = RegressionModel(X, y)
        model.calculate_beta()
        model.calculate_r2()
        model.calculate_normalized_coefficients()
        results = model.get_results()

        bot.reply_to(message, results)
        os.remove("received_file.txt")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

bot.polling()