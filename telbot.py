import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
import sqlite3 as sl

bot = telebot.TeleBot('6673879527:AAGKIM0bC1Aqqk2uhKkx5w71Yupa2WBYYhg');
global user
user = []

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

def menu_gen():
    con = sl.connect('tgbase.db')
    categ_k = con.execute(f"SELECT name FROM CATEGORY").fetchall()
    keyb = InlineKeyboardMarkup()
    for i in range(len(categ_k)):
        keyb.add(InlineKeyboardButton(list(categ_k[i])[0], callback_data="m"+str(i+1)))
    return keyb




# Запуск бота и проверка на регистрацию
@bot.message_handler(commands=['start'])
def start(message):
    con = sl.connect('tgbase.db')
    user_list = con.execute(f"SELECT id_telegram FROM USERS").fetchall()
    user_id = ""
    for i in user_list:
        user_id += str(i)
    if message.text == '/start':
        if str(message.from_user.id) in user_id:
            answ = bot.send_message(message.chat.id,
                         text="Добро пожаловать в бот ресторан.",
                         reply_markup=create_keyboard_2())
            bot.register_next_step_handler(answ,menu)
        else:
            regstr = bot.send_message(message.chat.id,
                         text="Добро пожаловать в бот ресторан нажми кнопку регистрации чтобы продолжить.", reply_markup=create_keyboard_1())
            bot.register_next_step_handler(regstr,reg)
@bot.message_handler(content_types=['text'])

def reg(message):

    if message.text == "Регистрация 👋":
        bot.send_message(message.chat.id, text="Введите свое имя c большой буквы")
        user.append(message.from_user.id)

    elif message.text.istitle():
        user.append(message.text)
        bot.send_message(message.chat.id, text="Введите свой номер телефона начиная с +375")

    elif "+375" in message.text:
        user.append(message.text)
        bot.send_message(message.chat.id, text="Введите свой адрес доставки начиная с ул.")

    elif "ул." in message.text:
        user.append(message.text)
        bot.send_message(message.chat.id, text="Регистрация завершена",reply_markup=create_keyboard_2())
        con = sl.connect('tgbase.db')
        with con:
            con.execute("INSERT OR IGNORE INTO USERS (id_telegram,name,tel,address) values(?, ?, ?, ?)", user)

    else:
        bot.send_message(message.chat.id, text="Что-то пошло не так попробуй еще раз")
        return


def menu(message):
    # Меню
    if message.text == "Меню 📜":
        answer = bot.send_message(message.chat.id, text="Выберисте категорию",reply_markup=menu_gen())
        bot.register_next_step_handler(answer, menu)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id,)
    id = call.message.chat.id
    flag = call.data[0]
    data = call.data[1:]
    print(flag,data)
    # if flag == "m":
    #     num = int(data)
    #     text = ""
    #     for i in [0,2,3,4,5]:
    #         text += f"{head[i]} {list_of_lists[num][i]}\n"
    #     bot.send_message(call.message.chat.id,text)









print("Ready")
bot.infinity_polling()