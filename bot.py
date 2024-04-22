import telebot #type: ignore
import numpy as np
import matplotlib.pyplot as plt
import io
from telebot import types # type: ignore

bot = telebot.TeleBot('7085664283:AAGOvJZrr1nJXIKgD2hMGkkCX8_ehURWEg0')

@bot.message_handler(commands=['Регрессия', 'регрессия'])
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
            bot.register_next_step_handler(message, xi, yi)
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
            description = f'Получаем теоретическое уравнение регрессии, имеющее следующий вид: \n\ny = {b:.2f}x + {a:.2f} \n\nЯ могу построить дополнительный график с отметками всех точек xi, yi. Необходимо ли это?'
            x = np.linspace(-10, 10, 100)
            y = a * x + b
            plt.switch_backend('Agg')
            fig = plt.figure()
            plt.plot(x, y)
            plt.title('Линейная регрессия')
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            markup = types.InlineKeyboardMarkup()
            button_yes = types.InlineKeyboardButton(text = 'Построить график', callback_data='yes_graph')
            markup.add(button_yes)
            bot.send_photo(message.chat.id, photo=buf, caption=description, reply_markup=markup)
            plt.close(fig)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат ввода. Пожалуйста, введите числа, разделенные пробелом.")

@bot.callback_query_handler(func=lambda call: True)
def response(function_call, xi, yi):
    if function_call.message:
        if function_call.data == 'yes_graph':
            second_message = 'Вот дополнительный график, содержащий точки xi, yi'
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
            x = np.linspace(-10, 10, 100)
            y = a * x + b
            plt.switch_backend('Agg')
            fig = plt.figure()
            plt.plot(x, y)
            plt.scatter(xi, yi, color='red', label='Точки xi, yi')
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.tight_layout()
            plt.title('Линейная регрессия с точками xi, yi')
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            bot.send_message(function_call.chat.id, second_message)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('Регрессия')
    button4 = types.KeyboardButton('Дополнительно')
    markup.add(button2, button4)
    photo_lnk = open('img/tst.jpg', 'rb')
    caption = 'Привет, я RegressionBot. Смогу помочь тебе разобраться с регрессионным анализом и решить задачи с различным количеством входных данных'
    bot.send_photo(message.chat.id, photo_lnk, caption, reply_markup=markup)
    photo_lnk.close()

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'График':
        pass

bot.polling()