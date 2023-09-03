from datetime import datetime
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
import sqlite3 as sl
from functools import partial
bot = telebot.TeleBot('6673879527:AAGKIM0bC1Aqqk2uhKkx5w71Yupa2WBYYhg')
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

def create_keyb_5(b):
    keyb_5 = InlineKeyboardMarkup()
    one_btn = types.InlineKeyboardButton(text="Изменить кол-во", callback_data='8'+str(b))
    two_btn = types.InlineKeyboardButton(text="Подтвердить заказ", callback_data='9')
    tree_btn = types.InlineKeyboardButton(text="Удалить из корзины", callback_data='q'+str(b))
    keyb_5.add(one_btn,two_btn,tree_btn)
    return keyb_5

def create_keyb_6(dish,orders):
    keyb_6 = InlineKeyboardMarkup()
    for i in range(len(dish)):
        keyb_6.add(InlineKeyboardButton(str(dish[i]), callback_data=f"b+{orders}" + str(dish[i])))
    return keyb_6

def create_keyb_7(dish,orders):
    keyb_7 = InlineKeyboardMarkup()
    for i in range(len(dish)):
        keyb_7.add(InlineKeyboardButton(str(dish[i]), callback_data=f'u+{orders}' + str(dish[i])))
    return keyb_7

def create_keyb_8():
    con = sl.connect('tgbase.db')
    dish = con.execute(f"SELECT id, name FROM DISHES ").fetchall()
    keyb_8 = InlineKeyboardMarkup()
    for i in range(len(dish)):
        keyb_8.add(
            InlineKeyboardButton("Блюдо № " + str(dish[i][0]) + " " + str(dish[i][1]),
                                 callback_data="X" + str(dish[i][0])))
    return keyb_8

def adminusers(a):
    keyb_users_rem = InlineKeyboardMarkup()
    one_btn = types.InlineKeyboardButton(text="Изменить имя", callback_data='c1'+str(a))
    two_btn = types.InlineKeyboardButton(text="Изменить адрес доставки", callback_data='c2'+str(a))
    three_btn = types.InlineKeyboardButton(text="Изменить должность", callback_data='c3'+str(a))
    four_btn = types.InlineKeyboardButton(text="Изменить телефон", callback_data='c4'+str(a))
    keyb_users_rem.add(one_btn, two_btn, three_btn,four_btn)
    return keyb_users_rem

def admindish(a):
    keyb_dish = InlineKeyboardMarkup()
    one_btn = types.InlineKeyboardButton(text="Изменить имя", callback_data='s1' + str(a))
    two_btn = types.InlineKeyboardButton(text="Изменить вес", callback_data='s2' + str(a))
    three_btn = types.InlineKeyboardButton(text="Изменить стоимость", callback_data='s3' + str(a))
    four_btn = types.InlineKeyboardButton(text="Изменить описание", callback_data='s4' + str(a))
    five_btn = types.InlineKeyboardButton(text="Изменить фото", callback_data='s5' + str(a))
    six_btn = types.InlineKeyboardButton(text="Изменить категорию", callback_data='s6' + str(a))
    seven_btn = types.InlineKeyboardButton(text="Изменить время приготовления", callback_data='s7' + str(a))
    eight_btn = types.InlineKeyboardButton(text="Изменить рейтинг", callback_data='s8' + str(a))
    nine_btn = types.InlineKeyboardButton(text="Поставить или снять 'STOP'", callback_data='s9' + str(a))
    keyb_dish.add(one_btn, two_btn, three_btn, four_btn,five_btn)
    keyb_dish.add(six_btn, seven_btn, eight_btn,nine_btn)
    return keyb_dish

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
@bot.message_handler(commands=['admin','adminusers','admincateg','adminorders','admindish','statis'])

def admin(message):
    post_levl_1 =['Доступные комманды суперадмина','Редактирование пользователей /adminusers',
                  'Редактирорвание категорий блюд /admincateg','Редактирование блюд /admindish',
                  'Редактирование заказов /adminorders','Статистика /statis']
    post_levl_2 =['Доступные комманды админа помощника',
                  'Редактирорвание категорий блюд /admincateg','Редактирование блюд /admindish',
                  'Редактирование заказов /adminorders','Статистика /statis']
    con = sl.connect('tgbase.db')
    post = con.execute(f"SELECT post FROM USERS WHERE id_telegram = {message.from_user.id}").fetchall()
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

    elif message.text =="/adminorders":
        if post[0][0] == 1 or post[0][0] == 2:
            orders = con.execute(f"SELECT id, user FROM ORDERS ").fetchall()
            keyb_orders = InlineKeyboardMarkup()
            for i in range(len(orders)):
                keyb_orders.add(
                    InlineKeyboardButton("№ заказа " + str(orders[i][0]) + " id_user" + str(orders[i][1]), callback_data="e" + str(orders[i][0])))
            bot.send_message(message.chat.id, text=f'Выберите заказ', reply_markup=keyb_orders)

    elif message.text =="/admindish":
        if post[0][0] == 1 or post[0][0] == 2:
            keyb_dish = InlineKeyboardMarkup()
            one_btn = types.InlineKeyboardButton(text="Добавить новое блюдо", callback_data='hv1')
            two_btn = types.InlineKeyboardButton(text="Изменить существующее блюдо", callback_data='hv2')
            keyb_dish.add(one_btn, two_btn)
            bot.send_message(message.chat.id, text=f'Выберите действие', reply_markup=keyb_dish)

    elif message.text =="/statis":
        if post[0][0] == 1 or post[0][0] == 2:
            list_static = []
            con = sl.connect('tgbase.db')
            kol_vo_us = con.execute(f"SELECT id FROM USERS ").fetchall()
            kol_vo_ord = con.execute(f"SELECT id FROM ORDERS WHERE payment = {1}").fetchall()
            slov_static = {'Кол-во зарегистрированых пользователей':len(kol_vo_us), 'Кол-во выполненых заказов':len(kol_vo_ord)}
            for k, v in slov_static.items():
                list_static.append(k + ': ' + str(v))
            vivod = '\n'.join(list_static)
            bot.send_message(message.chat.id, text=f"{'Статистика 📒'}\n{vivod}")

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

# Меню
def menu(message):
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
            bot.send_message(message.chat.id, text=f'{a}', reply_markup=create_keyb_5(id_order[0][0]))
        except:
            bot.send_message(message.chat.id, text=f'Ваша корзина пуста')

# Изменение кол-во блюд в корзине
def change(message):
    con = sl.connect('tgbase.db')
    id_dish = con.execute(f"SELECT id FROM DISHES WHERE name = '{bbb['flag'][1:]}'").fetchall()
    with con:
        con.execute(f"UPDATE GOODS SET kol_vo_dishes ={int(message.text)} WHERE dishes = {int(id_dish[0][0])} AND orders = {int(bbb['flag'][0])}")
    bot.send_message(message.chat.id, text=f'Кол-во было изменено')

def delete_kor(grus):
    con = sl.connect('tgbase.db')
    id_dish = con.execute(f"SELECT id FROM DISHES WHERE name = '{grus[1:]}'").fetchall()
    with con:
        con.execute(f"DELETE FROM GOODS WHERE dishes = {int(id_dish[0][0])} AND orders = {int(grus[0])}")

# Заказы
def ord(message):
    list_dict = []
    con = sl.connect('tgbase.db')
    id_order = con.execute(f"SELECT id FROM ORDERS WHERE user = {message.json['chat']['id']}").fetchall()
    for i in id_order:
        data = 15
        ammout = 0
        vv = []
        slov_mess = {}
        spis = ['Номер заказа', 'Время доставки заказа', 'Статус оплаты', 'Дата заказа']
        orders = con.execute(f"SELECT id,time_deliv,payment,date FROM ORDERS  WHERE id ={i[0]} GROUP BY id").fetchall()
        id_dish = con.execute(f"SELECT dishes, kol_vo_dishes FROM GOODS WHERE orders ={i[0]}").fetchall()
        if len(id_dish) != 0:
            a = orders+id_dish
            slov_mess = dict(zip(spis, a[0]))
            for n in a[1:]:
                dish = con.execute(f"SELECT name, price, cooking_time FROM DISHES WHERE id ={n[0]}").fetchall()
                ammout += int(dish[0][1][:2])*n[1]
                data += int(dish[0][2])
                vv.append(dish[0][0]+f", Кол-во блюд = {str(n[1])}")
                slov_mess["Блюда"] = '\n'.join(vv)
        if len(slov_mess) != 0:
            slov_mess["Общая стоимость"] = ammout
            slov_mess["Время доставки заказа"] = data
            slov_mess["Дата заказа"] = datetime.fromtimestamp(slov_mess["Дата заказа"])
            if slov_mess["Статус оплаты"] == 1:
                slov_mess['Статус оплаты'] = "Оплачен"
            else:
                slov_mess['Статус оплаты'] = "Не оплачен"
        for k, v in slov_mess.items():
            list_dict.append(k + ': ' + str(v))
    vivod = '\n'.join(list_dict)
    keyb = InlineKeyboardMarkup()
    one_btn = types.InlineKeyboardButton(text="Отменить заказ", callback_data='R')
    two_btn = types.InlineKeyboardButton(text="Оценить блюдо", callback_data='L')
    keyb.add(one_btn,two_btn)
    bot.send_message(message.chat.id, text=f"{'Ваши заказы 📒'}\n{vivod}", reply_markup=keyb)

def orders_delete(message):
    con = sl.connect('tgbase.db')
    print(message.json['text'])
    with con:
        con.execute(f"DELETE FROM ORDERS WHERE user = {message.json['chat']['id']} AND id = {int(message.json['text'])}")
    bot.send_message(message.chat.id, text=f"Ваш заказ успешно отменен")

#Отправка сообщений в группу поддержки
def support(message):
    bot.send_message(-1001980704979, text=f"{message.chat.username} просит о помощи \n{message.text}")
    create_keyboard_2()

#Редактирование Пользователей (панель админа)
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

#Редактирование и создание категорий блюд (панель администратора)
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

# Редактирование заказов(панель админа)
def orders_change(message):
    con = sl.connect('tgbase.db')
    with con:
        con.execute(f"UPDATE ORDERS SET payment = {int(message.text)} WHERE id = {int(user_bbb['e'])}")
    bot.send_message(message.chat.id,text=f"Оплата для заказа № {user_bbb['e']} изменена. Для возврата в меню админа /admin")

# Редактирование блюд
def dish_change(message):
    con = sl.connect('tgbase.db')
    if user_bbb['s'][0] == "1":
        with con:
            con.execute(f"UPDATE DISHES SET name = '{message.text}' WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"Имя блюда изменено на {message.text}. Для возврата в меню админа /admin")

    elif user_bbb['s'][0] == "2":
        with con:
            con.execute(f"UPDATE DISHES SET weight = '{message.text}' WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"Вес блюда изменен на {message.text}. Для возврата в меню админа /admin")

    elif user_bbb['s'][0] == "3":
        with con:
            con.execute(f"UPDATE DISHES SET price = '{message.text}' WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"Стоимость блюда изменена на {message.text}. Для возврата в меню админа /admin")

    elif user_bbb['s'][0] == "4":
        with con:
            con.execute(f"UPDATE DISHES SET description = '{message.text}' WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"Описание блюда изменено. Для возврата в меню админа /admin")

    elif user_bbb['s'][0] == "5":
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'C:/Users/ReDWaR/PycharmProjects/pythonProject_telebot/photo/' + message.photo[1].file_id
        with open(src+".png",'wb') as new_file:
            new_file.write(downloaded_file)
        with con:
            con.execute(f"UPDATE DISHES SET photo = '{message.photo[1].file_id}' WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"Фото блюда изменено. Для возврата в меню админа /admin")

    elif user_bbb['s'][0] == "6":
        with con:
            con.execute(f"UPDATE DISHES SET category = {int(message.text)} WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"Категория блюда изменена. Для возврата в меню админа /admin")

    elif user_bbb['s'][0] == "7":
        with con:
            con.execute(f"UPDATE DISHES SET cooking_time = {message.text} WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"Время приготовления блюда изменено. Для возврата в меню админа /admin")

    elif user_bbb['s'][0] == "8":
        with con:
            con.execute(f"UPDATE DISHES SET rating = {int(message.text)} WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"Рейтинг блюда изменен. Для возврата в меню админа /admin")

    elif user_bbb['s'][0] == "9":
        with con:
            con.execute(f"UPDATE DISHES SET stoped = {int(message.text)} WHERE id = {int(user_bbb['s'][1])}")
        bot.send_message(message.chat.id,text=f"'Stop' блюда изменен. Для возврата в меню админа /admin")

def dish_add(message):
    con = sl.connect('tgbase.db')
    with con:
        con.execute(f"INSERT OR IGNORE INTO DISHES (name,stoped) values('{message.text}',{0})")
    bot.send_message(message.chat.id, text=f"Блюдо успешно добавлено. Для возврата в меню админа /admin")

def rating(message):
    con = sl.connect('tgbase.db')
    if 0 < int(message.text) <= 5:
        with con:
            con.execute(f"INSERT OR IGNORE INTO RATING (dish,rating) values({int(message.text)},{int(user_bbb['FFF'])})")
        bot.send_message(message.chat.id, text=f"Спасибо за вашу оценку")
    else:
        bot.send_message(message.chat.id, text=f"Некорректное число")
        bot.send_message(message.chat.id, text=f'Выберите блюдо', reply_markup=create_keyb_8())


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id,)
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
        a = []
        sr = ""
        num = int(data)
        dish = con.execute(f"SELECT photo,name,weight,description,price FROM DISHES WHERE stoped={0}").fetchall()
        rating = con.execute(f"SELECT rating FROM rating WHERE dish = {num}").fetchall()
        for x in range(len(rating)):
            a.append(rating[x][0])
        rating_list = f"Рейтинг блюда: {(4+int(sum(a)))/len(rating)}"
        photo = open(f"C:/Users/ReDWaR/PycharmProjects/pythonProject_telebot/photo/{dish[num - 1][0]}.png", 'rb')
        for a in dish[num-1][1:5]:
            sr += f'{str(a)}\n'
        bot.send_photo(call.message.chat.id, photo)
        bot.send_message(call.message.chat.id,text=f'№{num}\n{sr}{rating_list}',reply_markup=create_keyb_4(1,num))

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
        a = []
        sr = ""
        num = int(data)+1
        dish = con.execute(f"SELECT photo,name,weight,description,price FROM DISHES WHERE stoped = {0}").fetchall()
        rating = con.execute(f"SELECT rating FROM rating WHERE dish = {num}").fetchall()
        for x in range(len(rating)):
            a.append(rating[x][0])
        rating_list = f"Рейтинг блюда: {(4+int(sum(a)))/len(rating)}"
        photo = open(f"C:/Users/ReDWaR/PycharmProjects/pythonProject_telebot/photo/{dish[num - 1][0]}.png", 'rb')
        for a in dish[num - 1][1:5]:
            sr += f'{str(a)}\n'
        bot.send_photo(call.message.chat.id, photo)
        bot.send_message(call.message.chat.id, text=f'№{num}\n{sr}{rating_list}', reply_markup=create_keyb_4(1,num))

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
        id_order = call.data[1:]
        bot.send_message(call.message.chat.id, text=f'Выбери блюдо', reply_markup=create_keyb_6(a,id_order))

    if flag =="q":
        text = call.message.json["text"]
        lists = text.split("\n")
        a = lists[::2]
        id_ord = call.data[1:]
        bot.send_message(call.message.chat.id, text=f'Выбери блюдо', reply_markup=create_keyb_7(a,id_ord))

    if flag == "u":
        delete_kor(call.data[2:])

    if flag == "R":
        z = bot.send_message(call.message.chat.id, text=f'Введи номер заказа', )
        bot.register_next_step_handler(z, orders_delete)

    if flag == "9":
        id_user = call.message.json["chat"]["id"]
        ord_date = call.message.json["date"]
        user.append(id_user)
        with con:
            con.execute(f"INSERT OR IGNORE INTO ORDERS (user,date) values({int(id_user)},{ord_date})")
        bot.send_message(call.message.chat.id, text=f'Ваш заказ подтвержден перейдите во вкладку мои заказы')

    if flag == "b":
        bbb["flag"] = call.data[2:]
        z = bot.send_message(call.message.chat.id, text=f'Введи кол-во',)
        bot.register_next_step_handler(z,change)

    if flag =="a":
        bot.send_message(call.message.chat.id, text=f'Выберите действие',reply_markup=adminusers(data))

    if flag =="c":
        user_bbb['c'] = data
        if call.data[1] == "3":
            g = bot.send_message(call.message.chat.id,text=f'Введите должность Где: 0-Пользователь, 2-Администратор/помошник')
            bot.register_next_step_handler(g, users_change)

        else:
            g = bot.send_message(call.message.chat.id, text=f'Введите изменения')
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

    if flag == "e":
        user_bbb['e'] = data
        x = bot.send_message(call.message.chat.id, text=f'Введите статус оплаты где 0-Не оплачен, 1-Оплачен')
        bot.register_next_step_handler(x, orders_change)

    if flag == "h":
        if call.data[1:] == "v1":
            f = bot.send_message(call.message.chat.id, text=f'Введите название нового блюда, а затем с помощью панели админа отредактируйте.')
            bot.register_next_step_handler(f, dish_add)

        elif call.data[1:] =="v2":
            dish = con.execute(f"SELECT id, name FROM DISHES ").fetchall()
            keyb_dish = InlineKeyboardMarkup()
            for i in range(len(dish)):
                keyb_dish.add(
                    InlineKeyboardButton("Блюдо № " + str(dish[i][0]) + " " + str(dish[i][1]), callback_data="k" + str(dish[i][0])))
            bot.send_message(call.message.chat.id, text=f'Выберите блюдо', reply_markup=keyb_dish)

    if flag == "k":
        bot.send_message(call.message.chat.id, text=f'Выберите действие', reply_markup=admindish(data))

    if flag == "s":
        user_bbb['s'] = data
        if data[0] == "9":
            user_bbb['s'] = data
            y = bot.send_message(call.message.chat.id, text=f'Введите значение для "STOP" где 0-Блюдо в меню 1-Блюдо на стопе')
            bot.register_next_step_handler(y, dish_change)
        else:
            y = bot.send_message(call.message.chat.id, text=f'Введите изменения(или загрузите фото)')
            bot.register_next_step_handler(y, dish_change)

    if flag == "L":
        bot.send_message(call.message.chat.id, text=f'Выберите блюдо', reply_markup=create_keyb_8())

    if flag == "X":
        user_bbb['FFF'] = call.data[1]
        x = bot.send_message(call.message.chat.id, text=f'Введите как вы оцниваете блюдо по шкале от 1 до 5.')
        bot.register_next_step_handler(x, rating)




print("Ready")
bot.infinity_polling()