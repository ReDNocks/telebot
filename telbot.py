import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto


bot = telebot.TeleBot('6673879527:AAGKIM0bC1Aqqk2uhKkx5w71Yupa2WBYYhg');

def create_keyboard_1():
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Регистрация 👋")
    markup1.add(btn1)
    return markup1

def create_keyboard_2():
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Меню 📜")
    btn2 = types.KeyboardButton("Корзина 🛒")
    btn3 = types.KeyboardButton("Поддержка ❓")
    btn4 = types.KeyboardButton("Мои заказы 📒")
    markup2.add(btn1, btn2,btn3,btn4)
    return markup2
def create_keyboard_3():
    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("ОК 🆗")
    markup3.add(btn1)
    return markup3

@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         text="Добро пожаловать в бот ресторан нажми кнопку регистрации чтобы продолжить.", reply_markup=create_keyboard_1())

@bot.message_handler(content_types=['text'])
def reg(message):

    if message.text == "Регистрация 👋":
        bot.send_message(message.chat.id, text="Введите свое имя c большой буквы")
        print(message)
    elif message.text.istitle():
        bot.send_message(message.chat.id, text="Введите свой номер телефона начиная с +375")
        print(message)

    elif "+375" in message.text:
        bot.send_message(message.chat.id, text="Введите свой адрес доставки")
        print(message)
    elif "+375" not in message.text:
        bot.send_message(message.chat.id, text="Что-то пошло не так попробуй еще раз")
        return


print("Ready")
bot.infinity_polling()