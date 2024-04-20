import telebot #type: ignore
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
import urllib.request
from telebot import types # type: ignore

bot = telebot.TeleBot('7085664283:AAGOvJZrr1nJXIKgD2hMGkkCX8_ehURWEg0')

@bot.message_handler(commands=['regress'])
def regress(message):
    bot.send_message(message.chat.id, "Пожалуйста, введите значения xi, разделенные пробелом:")
    bot.register_next_step_handler(message, get_xi)

def get_xi(message):
    try:
        xi = [float(i) for i in message.text.split()]
        bot.send_message(message.chat.id, "Теперь введите значения yi, разделенные пробелом:")
        bot.register_next_step_handler(message, get_yi, xi)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода. Пожалуйста, введите числа, разделенные пробелом.")

def get_yi(message, xi):
    try:
        yi = [float(i) for i in message.text.split()]
        if len(xi) != len(yi):
            bot.send_message(message.chat.id, "Количество значений xi и yi должно совпадать.")
        else:
            x = np.zeros((len(xi), 2))
            x[:, 0] = 1
            x[:, 1] = xi
            x_t = x.T
            y = np.array(yi).reshape(-1, 1)
            product = x_t @ x
            product_inv = np.linalg.inv(product)
            result = product_inv @ x_t @ y
            a = result[0][0]
            b = result[1][0]
            bot.send_message(message.chat.id, f'y = {b:.2f}x + {a:.2f}')
            bot.register_next_step_handler(message, visual_graph, a, b)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода. Пожалуйста, введите числа, разделенные пробелом.")

def visual_graph(message, a, b):
    x = np.linspace(-10, 10, 100)
    y = a * x + b
    fig = plt.figure()
    plt.plot(x, y)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    bot.send_photo(message.chat.id, photo=buf)
    plt.close(fig)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('О проекте')
    button2 = types.KeyboardButton('Регрессия')
    button3 = types.KeyboardButton('Анализ')
    button4 = types.KeyboardButton('Дополнительно')
    markup.add(button1, button2, button3, button4)
    photo_lnk = open('img/tst.jpg', 'rb')
    caption = 'Привет, я RegressionBot. Смогу помочь тебе разобраться с регрессионным анализом и решить задачи с различным количеством входных данных'
    bot.send_photo(message.chat.id, photo_lnk, caption, reply_markup=markup)
    photo_lnk.close()

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'График':
        visual_graph(message)

bot.polling()