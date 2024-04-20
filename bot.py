import telebot #type: ignore

bot = telebot.TeleBot('7085664283:AAGOvJZrr1nJXIKgD2hMGkkCX8_ehURWEg0')

from telebot import types # type: ignore

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

bot.polling()
