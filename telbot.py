import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
import sqlite3 as sl
from functools import partial

bot = telebot.TeleBot('6673879527:AAGKIM0bC1Aqqk2uhKkx5w71Yupa2WBYYhg');
global user
user = []

#-1001980704979


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

def create_keyb_4(boon,dish):
    keyb_2 = InlineKeyboardMarkup()
    one_btn = types.InlineKeyboardButton(text="➕", callback_data='1')
    two_btn = types.InlineKeyboardButton(text="➖", callback_data='2')
    three_btn = types.InlineKeyboardButton(text="Заказать 📒", callback_data='3')
    four_btn = types.InlineKeyboardButton(text="Добавить в корзину 🛒", callback_data='4')
    five_btn = types.InlineKeyboardButton(text="Следующее блюдо ➡️", callback_data="z"+str(dish))
    six_btn = types.InlineKeyboardButton(text=f"{boon}", callback_data='6')
    keyb_2.add(two_btn,six_btn,one_btn)
    keyb_2.add(three_btn,four_btn)
    keyb_2.add(five_btn)
    return keyb_2


def create_keyb_5():
    keyb_5 = InlineKeyboardMarkup()
    one_btn = types.InlineKeyboardButton(text="Изменить кол-во", callback_data='8')
    two_btn = types.InlineKeyboardButton(text="Подтвердить заказ", callback_data='9')
    keyb_5.add(one_btn,two_btn)
    return keyb_5

def create_keyb_6(dish):
    keyb_6 = InlineKeyboardMarkup()
    for i in range(len(dish)):
        print(i)
        keyb_6.add(InlineKeyboardButton(str(dish[i]), callback_data="b" + str(i + 1)))
    return keyb_6

def adminusers(a):
    keyb_users_rem = InlineKeyboardMarkup()
    one_btn = types.InlineKeyboardButton(text="Изменить имя", callback_data='c1'+str(a))
    two_btn = types.InlineKeyboardButton(text="Изменить адрес доставки", callback_data='c2'+str(a))
    three_btn = types.InlineKeyboardButton(text="Изменить должность", callback_data='c3'+str(a))
    four_btn = types.InlineKeyboardButton(text="Изменить телефон", callback_data='c4'+str(a))
    keyb_users_rem.add(one_btn, two_btn, three_btn,four_btn)
    return keyb_users_rem


# Запуск бота и проверка на регистрацию
@bot.message_handler(commands=['start'])
def start(message):
    con = sl.connect('tgbase.db')
    user_list = con.execute(f"SELECT id_telegram FROM USERS").fetchall()
    user_id = ""
    dicty = {"chat_id":message.chat.id,"text":"Добро пожаловать в бот ресторан.",
             "reply_markup":create_keyboard_2()}

    for i in user_list:
        user_id += str(i)
    if message.text == '/start':
        if str(message.from_user.id) in user_id:
            answ = bot.send_message(**dicty)
            bot.register_next_step_handler(answ,menu)
        else:
            regstr = bot.send_message(message.chat.id,
                         text="Добро пожаловать в бот ресторан нажми кнопку регистрации чтобы продолжить.", reply_markup=create_keyboard_1())
            bot.register_next_step_handler(regstr,reg)


bbb = {}
user_bbb = {}

# БЛОК АДМИН ПАНЕЛИ
@bot.message_handler(commands=['admin','adminusers','admincateg'])

def admin(message):
    post_levl_1 =['Доступные комманды суперадмина','Редактирование пользователей /adminusers',
                  'Редактирорвание категорий блюд /admincateg','Редактирование блюд /admindish',
                  'Редактирование заказов /adminorders']
    post_levl_2 =['Доступные комманды админа помощника',
                  'Редактирорвание категорий блюд /admincateg','Редактирование блюд /admindish',
                  'Редактирование заказов /adminorders']
    con = sl.connect('tgbase.db')
    post = con.execute(f"SELECT post FROM USERS").fetchall()

    if message.text =="/admin":
        if post[0][0] == 1:
            v = '\n'.join(post_levl_1)
            bot.send_message(message.chat.id, text=f'{v}')
        elif post[0][0] == 2:
            v = '\n'.join(post_levl_2)
            bot.send_message(message.chat.id, text=f'{v}')
        else:
            bot.send_message(message.chat.id, text=f'У вас нет прав для данной команды')

    elif message.text =="/adminusers":
        if post[0][0] == 1:
            users = con.execute(f"SELECT id_telegram, name FROM USERS").fetchall()
            keyb_user = InlineKeyboardMarkup()
            for i in range(len(users)):
                keyb_user.add(
                    InlineKeyboardButton("id " + users[i][0] + " " + users[i][1], callback_data="a" + str(users[i][0])))
            bot.send_message(message.chat.id, text=f'Выберите пользователя', reply_markup=keyb_user)

    elif message.text =="/admincateg":
        if post[0][0] == 1 or post[0][0] == 2:
            keyb_categ = InlineKeyboardMarkup()
            one_btn = types.InlineKeyboardButton(text="Добавить новую категорию", callback_data='dl1')
            two_btn = types.InlineKeyboardButton(text="Изменить существующую категорию", callback_data='dl2')
            keyb_categ.add(one_btn, two_btn)
            bot.send_message(message.chat.id, text=f'Выберите действие', reply_markup=keyb_categ)







@bot.message_handler(content_types=['text'])
# Регистрация
def reg(message):

    if message.text == "Регистрация 👋":
        con = sl.connect('tgbase.db')
        a = bot.send_message(message.chat.id, text="Введите свое имя c большой буквы")
        id_user = message.json["chat"]["id"]
        ord_date = message.json["date"]
        user.append(id_user)
        with con:
            con.execute(f"INSERT OR IGNORE INTO ORDERS (user,date) values({int(id_user)},{ord_date})")

    elif message.text == "Корзина 🛒":
        kor(message)

    elif message.text == "Меню 📜":
        menu(message)

    elif message.text == "Мои заказы 📒":
        ord(message)

    elif message.text == "Поддержка ❓":
        a = bot.send_message(message.chat.id, text="Напиши сообщение")
        bot.register_next_step_handler(a, support)

    elif message.text.istitle():
        user.append(message.text)
        bot.send_message(message.chat.id, text="Введите свой номер телефона начиная с +375")

    elif "+375" in message.text:
        user.append(message.text)
        bot.send_message(message.chat.id, text="Введите свой адрес доставки начиная с ул.")

    elif "ул." in message.text:
        user.append(message.text)
        sel = bot.send_message(message.chat.id, text="Регистрация завершена",reply_markup=create_keyboard_2())
        bot.register_next_step_handler(sel, menu)
        con = sl.connect('tgbase.db')
        with con:
            con.execute("INSERT OR IGNORE INTO USERS (id_telegram,name,tel,address) values(?, ?, ?, ?)", user)

    else:
        fol = bot.send_message(message.chat.id, text="Что-то пошло не так попробуй еще раз")
        bot.register_next_step_handler(fol, reg)
        return


def menu(message):
    # Меню
    answer = bot.send_message(message.chat.id, text="Выберисте категорию",reply_markup=menu_gen())

# Корзина
def kor(message):
    if message.text == "Корзина 🛒":
        try:
            korzinka = []
            con = sl.connect('tgbase.db')
            max_data = con.execute(f"SELECT MAX(date) FROM ORDERS WHERE user = {message.json['chat']['id']} ").fetchall()
            id_order = con.execute(f"SELECT id FROM ORDERS WHERE user = {message.json['chat']['id']} and date = {max_data[0][0]}").fetchall()
            goods = con.execute(f"SELECT dishes,kol_vo_dishes FROM GOODS WHERE orders = {id_order[0][0]} ").fetchall()
            for i in range(len(goods)):
                dish = con.execute(f"SELECT id, name FROM DISHES WHERE id = {int(goods[i][0])} ").fetchall()
                korzinka.append(dish[0][1])
                korzinka.append(f"Кол-во блюд = {goods[i][1]}")
            a = "\n".join(korzinka)
            bot.send_message(message.chat.id, text=f'{a}', reply_markup=create_keyb_5())
        except:
            bot.send_message(message.chat.id, text=f'Ваша корзина пуста')

# Изменение кол-во блюд в корзине
def change(message):
    con = sl.connect('tgbase.db')
    with con:
        con.execute(f"UPDATE GOODS SET kol_vo_dishes ={int(message.text)} WHERE id = {int(bbb['flag'])}")

# Заказы
def ord(message):
    list_mess = []
    list_dict = []
    con = sl.connect('tgbase.db')
    id_user = message.json["chat"]["id"]
    orders = con.execute(f"SELECT * FROM ORDERS INNER JOIN GOODS ON ORDERS.id = GOODS.orders WHERE user ={id_user} ").fetchall()
    pay = con.execute(f"SELECT payment FROM ORDERS WHERE user = {message.json['chat']['id']}").fetchall()
    spis = ['Номер заказа','Время доставки заказа','USER:','Статус оплаты']
    id_order = con.execute(f"SELECT id FROM ORDERS WHERE user = {message.json['chat']['id']}").fetchall()
    a = 0
    b = 15
    # spis_mess[name_dish[0][0]] = str(orders[u][5:][2])+"-шт"
    # a = a+(float(name_dish[0][1][:2])*int(orders[u][7]))
    # b = b+(name_dish[0][2]*int(orders[u][7]))

    for u in range(len(orders)):
        if orders[u][:4] in list_mess:
            pass
        else:
            list_mess.append(orders[u][:4])
        # name_dish = con.execute(f"SELECT price,cooking_time FROM DISHES WHERE id = {orders[u][5:][1]}  ").fetchall()
        # name_dish.append(orders[u][5:][1])

    for i in range(len(list_mess)):
        slov_mess = dict(zip(spis,list_mess[i]))
        del slov_mess['USER:']
        if pay[0][0] == 0:
            slov_mess['Статус оплаты'] = "Не оплачен"
        else:
            slov_mess['Статус оплаты'] = "Оплачен"
        print(slov_mess)
        for k, v in slov_mess.items():
            list_dict.append(k + ': ' + str(v))
    v = '\n'.join(list_dict)
    bot.send_message(message.chat.id, text=f"{'Ваши заказы 📒'}\n{v}")

    # spis_mess['Время доставки заказа'] = str(b)+"-Минут"
    # spis_mess['Общая стоимость заказа'] = str(a)+"-рублей"


#Отправка сообщений в группу поддержки
def support(message):
    bot.send_message(-1001980704979, text=f"{message.chat.username} просит о помощи \n{message.text}")
    create_keyboard_2()


#Редактирование Имени(панель админа)
def users_change(message):
    con = sl.connect('tgbase.db')
    if user_bbb['c'][0] == "1":
        with con:
            con.execute(f"UPDATE USERS SET name = '{message.text}' WHERE id_telegram = {int(user_bbb['c'][1:])}")
        bot.send_message(message.chat.id, text=f"Имя изменено на {message.text} Для возврата в меню админа /admin")
    elif user_bbb['c'][0] == "2":
        with con:
            con.execute(f"UPDATE USERS SET address = '{message.text}' WHERE id_telegram = {int(user_bbb['c'][1:])}")
        bot.send_message(message.chat.id, text=f" Адрес доставки изменён на {message.text} Для возврата в меню админа /admin")
    elif user_bbb['c'][0] == "3":
        with con:
            con.execute(f"UPDATE USERS SET post = '{int(message.text)}' WHERE id_telegram = {int(user_bbb['c'][1:])}")
        bot.send_message(message.chat.id, text=f" Должность изменена на {message.text} Для возврата в меню админа /admin")

    elif user_bbb['c'][0] == "4":
        with con:
            con.execute(f"UPDATE USERS SET tel = '{message.text}' WHERE id_telegram = {int(user_bbb['c'][1:])}")
        bot.send_message(message.chat.id, text=f" Телефон изменён на {message.text} Для возврата в меню админа /admin")

#Редактирование и создание категорий блюд
def categ_change(message):
    con = sl.connect('tgbase.db')
    with con:
        con.execute(f"UPDATE CATEGORY SET name = '{message.text}' WHERE id = {int(user_bbb['d'])}")
    bot.send_message(message.chat.id, text=f" Имя категори изменено на  {message.text} Для возврата в меню админа /admin")

def categ_add(message):
    con = sl.connect('tgbase.db')
    with con:
        con.execute(f"INSERT OR IGNORE INTO CATEGORY (name) values('{message.text}')")
    bot.send_message(message.chat.id, text=f"Категория успешно создана с именем {message.text} Для возврата в меню админа /admin")









@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id,)
    id = call.message.chat.id
    flag = call.data[0]
    data = call.data[1:]
    con = sl.connect('tgbase.db')
    dish_k = con.execute(f"SELECT name,category FROM DISHES").fetchall()
    keyb_dish = InlineKeyboardMarkup()

    if flag == "m":
        num = int(data)
        for i in range(len(dish_k)):
            if num == list(dish_k[i])[1]:
                keyb_dish.add(InlineKeyboardButton(list(dish_k[i])[0], callback_data="n" + str(i + 1)))
        bot.send_message(call.message.chat.id, text="Выберите блюдо", reply_markup=keyb_dish)
    if flag == "n":
        sr = ""
        num = int(data)
        con = sl.connect('tgbase.db')
        dish = con.execute(f"SELECT photo,name,weight,description,price,stoped FROM DISHES").fetchall()
        for a in dish[num-1][1:5]:
            sr += f'{str(a)}\n'
        bot.send_photo(call.message.chat.id, dish[num - 1][0])
        bot.send_message(call.message.chat.id,text=f'№{num}\n{sr}',reply_markup=create_keyb_4(1,num))


    if flag == '1':
        text = call.message.json["reply_markup"]['inline_keyboard'][0][1]["text"]
        num = call.message.json["text"][1]
        bot.edit_message_reply_markup(
             chat_id=call.message.chat.id,
             message_id=call.message.message_id,
             reply_markup=create_keyb_4(int(text)+1,num))

    if flag == '2':
        text = call.message.json["reply_markup"]['inline_keyboard'][0][1]["text"]
        num = call.message.json["text"][1]
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_keyb_4(int(text)-1,num))

    if flag == 'z':
        sr = ""
        num = int(data)+1
        con = sl.connect('tgbase.db')
        dish = con.execute(f"SELECT photo,name,weight,description,price,stoped FROM DISHES").fetchall()
        for a in dish[num - 1][1:5]:
            sr += f'{str(a)}\n'
        bot.send_photo(call.message.chat.id, dish[num - 1][0])
        bot.send_message(call.message.chat.id, text=f'№{num}\n{sr}', reply_markup=create_keyb_4(1,num))

    if flag == "4":
        bot.send_message(call.message.chat.id, text="Товар успешно добавлен в корзину")
        spis = []
        id_dish = call.message.json["text"][1]
        kil_vo = call.message.json["reply_markup"]['inline_keyboard'][0][1]["text"]
        max_data = con.execute(f"SELECT MAX(date) FROM ORDERS WHERE user = {call.message.json['chat']['id']} ").fetchall()
        id_order = con.execute(f"SELECT id FROM ORDERS WHERE user = {call.message.json['chat']['id']} and date = {max_data[0][0]}").fetchall()
        spis.append(id_dish)
        spis.append(kil_vo)
        spis.append(id_order[0][0])
        with con:
            con.execute(f"INSERT OR IGNORE INTO GOODS (dishes,kol_vo_dishes,orders) values(?,?,?)",spis)


    if flag == "8":
        text = call.message.json["text"]
        lists = text.split("\n")
        a = lists[::2]
        bot.send_message(call.message.chat.id, text=f'Выбери блюдо', reply_markup=create_keyb_6(a))

    if flag == "9":
        con = sl.connect('tgbase.db')
        id_user = call.message.json["chat"]["id"]
        ord_date = call.message.json["date"]
        user.append(id_user)
        with con:
            con.execute(f"INSERT OR IGNORE INTO ORDERS (user,date) values({int(id_user)},{ord_date})")
        bot.send_message(call.message.chat.id, text=f'Ваш заказ подтвержден перейдите во вкладку мои заказы')

    if flag == "b":
        bbb["flag"] = data
        z = bot.send_message(call.message.chat.id, text=f'Введи кол-во',)
        bot.register_next_step_handler(z,change)

    if flag =="a":
        bot.send_message(call.message.chat.id, text=f'Выберите действие',reply_markup=adminusers(data))

    if flag =="c":
        if call.data[1] == "1":
            user_bbb['c'] = data
            g = bot.send_message(call.message.chat.id, text=f'Введите новое имя')
            bot.register_next_step_handler(g, users_change)

        elif call.data[1] == "2":
            user_bbb['c'] = data
            g = bot.send_message(call.message.chat.id, text=f'Введите новый адрес доставки начиная с ул.')
            bot.register_next_step_handler(g, users_change)

        elif call.data[1] == "3":
            user_bbb['c'] = data
            g = bot.send_message(call.message.chat.id, text=f'Введите должность Где: 0-Пользователь, 2-Администратор/помошник')
            bot.register_next_step_handler(g, users_change)

        elif call.data[1] == "4":
            user_bbb['c'] = data
            g = bot.send_message(call.message.chat.id, text=f'Введите новый телефон начиная с +375')
            bot.register_next_step_handler(g, users_change)

    if flag == "d":
        if call.data[1:] == "l1":
            f = bot.send_message(call.message.chat.id, text=f'Введите имя категории')
            bot.register_next_step_handler(f, categ_add)

        elif call.data[1:] == "l2":
            categ = con.execute(f"SELECT id, name FROM CATEGORY").fetchall()
            keyb_categ = InlineKeyboardMarkup()
            for i in range(len(categ)):
                keyb_categ.add(
                    InlineKeyboardButton("id " + str(categ[i][0]) + " " + str(categ[i][1]), callback_data="d" + str(categ[i][0])))
            bot.send_message(call.message.chat.id, text=f'Выберите категорию', reply_markup=keyb_categ)

        else:
            user_bbb['d'] = call.data[1:]
            v = bot.send_message(call.message.chat.id, text=f'Введите новое имя для категории')
            bot.register_next_step_handler(v, categ_change)























print("Ready")
bot.infinity_polling()