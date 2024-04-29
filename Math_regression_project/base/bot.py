import telebot
import math_path as mp
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
        button1 = types.KeyboardButton('Отправить файл')
        button2 = types.KeyboardButton('Ввести данные')
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

bot.polling()