from vk_api import VkApi
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3 as sl
import json

GROUP_ID = '220164616'
GROUP_TOKEN = 'vk1.a.TRTCFQ5vdI9-a7r-8uHgS9zEl6lZ_lreUO1KBO8MVl9kFN1XZBslqeiSdysXt_zWLMOXmIit0j3IC6Dhay7L7Dviw692R5X5Rarhd8B0SVOJ2ppkvQR14Sn0w_KBYvDUozV04bfVuAM7bUnDWoYgdCsLZRThhORAHf5gTZSZoDSFn20KRBxGGtpWAgmm0WNX5WssiHcHJsINBrMSWmYLew'
API_VERSION = '5.120'

# Запускаем бот
vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
vk_upload = VkUpload(vk)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
settings = dict(one_time=False, inline=False)
settings2 = dict(one_time=False, inline=True)

text_inst = """
1.Для начала работы нажмите : "Регистрация"
2.Если вы были ранее зарегистривоаны в нашем TeleGraM боте нажмите кнопку 'Проверить регистрацию'
"""
text_inst_2 = """
Дабро пожаловать в бот ресторан!!!!!!
"""
CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app', 'text')
HI = ["start","Start","начать","Начало","Начать","начало","Бот","бот","Старт","старт","скидки","Скидки"]
users = []

# ген
def keyb_1():
    keyb_1 = VkKeyboard(**settings)
    keyb_1.add_button(label='Регистрация 👋', color=VkKeyboardColor.NEGATIVE, payload={"type": "text"})
    keyb_1.add_line()
    keyb_1.add_button(label='Проверить регистрацию', color=VkKeyboardColor.POSITIVE, payload={"type": "text"})
    return keyb_1

def create_keyboard_2():
    create_keyboard_2 = VkKeyboard(**settings)
    create_keyboard_2.add_button(label="📜Меню", color=VkKeyboardColor.PRIMARY, payload={"type": "text"})
    create_keyboard_2.add_line()
    create_keyboard_2.add_button(label="🛒Корзина", color=VkKeyboardColor.PRIMARY, payload={"type": "text"})
    create_keyboard_2.add_line()
    create_keyboard_2.add_button(label="❓Поддержка ", color=VkKeyboardColor.PRIMARY, payload={"type": "text"})
    create_keyboard_2.add_line()
    create_keyboard_2.add_button(label="📒Мои заказы ", color=VkKeyboardColor.PRIMARY, payload={"type": "text"})
    return create_keyboard_2

def menu_gen(num):
    el_count = 5
    con = sl.connect('tgbase.db')
    categ_k = con.execute(f"SELECT name FROM CATEGORY").fetchall()
    keyb = VkKeyboard(**settings2)
    if el_count * (num + 1) < len(categ_k):
        maxi = el_count * (num + 1)
    else:
        maxi = len(categ_k)
    for a in range(num * el_count, maxi):
        keyb.add_callback_button(label=list(categ_k[a])[0], color=VkKeyboardColor.PRIMARY, payload={"categ": a+1})
        keyb.add_line()
    if num == 0:
        keyb.add_callback_button(label='Далее', color=VkKeyboardColor.PRIMARY, payload={"name_2": num + 1})
    elif el_count * (num + 1) >= len(categ_k):
        keyb.add_callback_button(label='Назад', color=VkKeyboardColor.PRIMARY, payload={"name_2": num - 1})
    else:
        keyb.add_callback_button(label='Далее', color=VkKeyboardColor.PRIMARY, payload={"name_2": num + 1})
        keyb.add_callback_button(label='Назад', color=VkKeyboardColor.PRIMARY, payload={"name_2": num - 1})
    return keyb

def create_keyb_3(boon,text,rat,name):
    create_keyb_3 = VkKeyboard(**settings2)
    create_keyb_3.add_callback_button(label="➖", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 2,"text":text,"rat":rat,"boon":boon,"name":name})
    create_keyb_3.add_callback_button(label=f"{str(boon)}", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 5})
    create_keyb_3.add_callback_button(label="➕", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 1,"text":text,"rat":rat,"boon":boon,"name":name})
    create_keyb_3.add_line()
    create_keyb_3.add_callback_button(label="Заказать 📒", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 3})
    create_keyb_3.add_callback_button(label="Добавить в корзину 🛒", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 4,"boon":boon,'name':name})
    create_keyb_3.add_line()
    create_keyb_3.add_callback_button(label="Следующее блюдо ➡️", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 6,"keyb_3_dish":name})
    return create_keyb_3

def create_keyb_5(b):
    create_keyb_5 = VkKeyboard(**settings2)
    create_keyb_5.add_callback_button(label="Изменить кол-во", color=VkKeyboardColor.PRIMARY, payload={"keyb_5": 1,"order":b})
    create_keyb_5.add_callback_button(label="Подтвердить заказ", color=VkKeyboardColor.PRIMARY, payload={"keyb_5": 2})
    create_keyb_5.add_line()
    create_keyb_5.add_callback_button(label="Удалить из корзины", color=VkKeyboardColor.PRIMARY, payload={"keyb_5": 3})
    return create_keyb_5

def create_keyb_6(id_order):
    good = con.execute(f"SELECT GOODS.id, dishes, name FROM GOODS JOIN DISHES ON GOODS.dishes=DISHES.id WHERE orders = {id_order}").fetchall()
    create_keyb_6 = VkKeyboard(**settings2)
    for i in range(len(good)):
        create_keyb_6.add_callback_button(label=f"{good[i][2]}", color=VkKeyboardColor.PRIMARY, payload={"keyb_6": 1,'dish':good[i][1],'good_id':good[i][0]})
    return create_keyb_6



#Смена id пользователя
def change_id_user(phone,obj):
    con = sl.connect('tgbase.db')
    try:
        with con:
            con.execute(f"UPDATE USERS SET id_vk = '{obj['from_id']}' WHERE tel = '{phone}'")
        vk.messages.send(
            user_id=obj['from_id'],
            random_id=get_random_id(),
            peer_id=obj['from_id'],
            keyboard=create_keyboard_2().get_keyboard(),
            message=text_inst_2)

    except:
        vk.messages.send(
            user_id=obj['from_id'],
            random_id=get_random_id(),
            peer_id=obj['from_id'],
            message="Пользователя не существует, пройдите регистрацию ")
#Каталог блюд
def dish_catalog(num):
    el_count = 5
    dish_k = con.execute(f"SELECT name,category FROM DISHES").fetchall()
    keyb_dish = VkKeyboard(**settings2)
    if el_count * num < len(dish_k):
        maxi = el_count * num
    else:
        maxi = len(dish_k)
    for i in range((num-1)*el_count, maxi):
        if num == list(dish_k[i])[1]:
            keyb_dish.add_callback_button(label=list(dish_k[i])[0], color=VkKeyboardColor.PRIMARY,payload={"dish": (dish_k[i])[0]})
            keyb_dish.add_line()
    if num == 1:
        keyb_dish.add_callback_button(label='Далее', color=VkKeyboardColor.PRIMARY, payload={"name_3": num + 1})
    elif el_count * num >= len(dish_k):
        keyb_dish.add_callback_button(label='Назад', color=VkKeyboardColor.PRIMARY, payload={"name_3": num - 1})
    else:
        keyb_dish.add_callback_button(label='Далее', color=VkKeyboardColor.PRIMARY, payload={"name_3": num + 1})
        keyb_dish.add_callback_button(label='Назад', color=VkKeyboardColor.PRIMARY, payload={"name_3": num - 1})
    return keyb_dish
#Блюдо
def dish(objec,num):
    bbb =[]
    a = []
    sr = ""
    dish_id = con.execute(f"SELECT id FROM DISHES WHERE stoped={0} AND name ='{objec}'").fetchone()
    try:
        rating = con.execute(f"SELECT rating FROM rating WHERE dish = {int(dish_id[0])+num}").fetchone()
        for x in range(len(rating)):
            a.append(rating[x])
        rating_list = (4 + int(sum(a))) / len(rating)
    except :
        rating_list = 4
    with con:
        con.execute(f"UPDATE DISHES SET rating = {int(rating_list)} WHERE id = {int(dish_id[0]+num)}")
    dish = con.execute(f"SELECT id,photo,name,weight,description,price,rating FROM DISHES WHERE stoped={0} AND id ={int(dish_id[0]+num)}").fetchone()
    photo = vk_upload.photo_messages(f"C:/Users/ReDWaR/PycharmProjects/pythonProject_telebot/photo/{dish[1]}.png")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    bbb.append(attachment)
    bbb.append(sr)
    for a in dish[2:6]:
        sr += f'{str(a)}\n'
    last_id = vk.messages.edit(
        attachment=attachment,
        peer_id=event.obj.peer_id,
        message=f'{sr}Рейтинг блюда: {dish[6]}',
        conversation_message_id=event.obj.conversation_message_id,
        keyboard=create_keyb_3(1,bbb,dish[6],dish[2]).get_keyboard())

# Корзина
def korzina(object):
    try:
        korzinka = []
        con = sl.connect('tgbase.db')
        id_user = con.execute(f"SELECT id FROM USERS WHERE id_vk = {int(object.obj.message['from_id'])} ").fetchone()
        max_data = con.execute(f"SELECT MAX(date) FROM ORDERS WHERE user = {id_user[0]} ").fetchone()
        id_order = con.execute(
            f"SELECT id FROM ORDERS WHERE user = {id_user[0]} and date = {max_data[0]}").fetchone()
        goods = con.execute(f"SELECT dishes,kol_vo_dishes FROM GOODS WHERE orders = {id_order[0]} ").fetchall()
        for i in range(len(goods)):
            dish = con.execute(f"SELECT id, name FROM DISHES WHERE id = {int(goods[i][0])} ").fetchall()
            korzinka.append(dish[0][1])
            korzinka.append(f"Кол-во блюд = {goods[i][1]}")
        a = "\n".join(korzinka)
        vk.messages.send(
            user_id=object.obj.message['from_id'],
            random_id=get_random_id(),
            peer_id=object.obj.message['from_id'],
            message=f'{a}',
            keyboard=create_keyb_5(id_order[0]).get_keyboard())
    except:
        vk.messages.send(
            user_id=object.obj.message['from_id'],
            random_id=get_random_id(),
            peer_id=object.obj.message['from_id'],
            message=f'Ваша корзина пуста', )


for event in longpoll.listen():
    con = sl.connect('tgbase.db')
    if event.type == VkBotEventType.MESSAGE_NEW: #Отлавливает сообщение

        if event.obj.message['text'] != '':

            if event.from_user:

                if event.obj.message['text'] in HI:
                    try:
                        user = con.execute(f"SELECT name FROM USERS WHERE id_vk = '{event.obj.message['from_id']}'")
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.obj.message['from_id'],
                            keyboard=create_keyboard_2().get_keyboard(),
                            message=text_inst_2)

                    except:
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.obj.message['from_id'],
                            keyboard=keyb_1().get_keyboard(),
                            message=text_inst)

                elif event.obj.message['text'] == 'Проверить регистрацию':
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        message="Введите номер телефона указанный при регистрации в формате +375")

                elif '+375' in event.obj.message['text']:
                    change_id_user(event.obj.message['text'], event.obj.message)

                elif event.obj.message['text'] == 'Регистрация 👋':
                    users.append(event.obj.message['from_id'])
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        message='Введите ваше имя с маленькой буквы')

                elif event.obj.message['text'].islower():
                    users.append(event.obj.message['text'].title())
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        message='Введите свой номер телефона начиная с 375')

                elif "375" in event.obj.message['text']:
                    plus = "+"
                    users.append(f'{plus}{event.obj.message["text"]}')
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        message="Введите свой адрес доставки начиная с Улица.")

                elif "Улица." in event.obj.message['text']:
                    try:
                        users.append(event.obj.message['text'])
                        con = sl.connect('tgbase.db')
                        with con:
                            con.execute("INSERT OR IGNORE INTO USERS (id_vk,name,tel,address) values(?, ?, ?, ?)", users)
                            con.execute(f"INSERT OR IGNORE INTO ORDERS (user,date) values({users[0]},{event.obj.message['date']})")
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.obj.message['from_id'],
                            message="Регистрация завершена")
                    except:
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.obj.message['from_id'],
                            message="Вы зарегистрированы проверте регистрацию")

                elif event.obj.message['text'] == "📜Меню":
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=menu_gen(num=0).get_keyboard(),
                        message="Категории блюд")

                elif event.obj.message['text'] == "🛒Корзина":
                    korzina(event)

                elif event.obj.message['text'] == "❓Поддержка":
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        message="Дарова корова")

                elif event.obj.message['text'] == "📒Мои заказы":
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        message="Дарова корова")

                else:
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        message="Что-то пошло не так попробуйте еще раз")

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('type') in CALLBACK_TYPES:
            vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps(event.object.payload))
        elif event.object.payload.get('name_2'):
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выберите категорию',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=menu_gen(event.object.payload.get("name_2")).get_keyboard())

        elif event.object.payload.get('name_3'):
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выберите блюдо',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=dish_catalog(event.object.payload.get("name_3")).get_keyboard())

        elif event.object.payload.get('categ'):
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выберите блюдо',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=dish_catalog(event.object.payload.get('categ')).get_keyboard())

        elif event.object.payload.get('dish'):
            dish(event.object.payload.get('dish'), 0)

        elif event.object.payload.get("keyb_3") == 1:
            last_id = vk.messages.edit(
                peer_id=event.object.peer_id,
                attachment=event.object.payload.get("text")[0],
                message=f'{event.object.payload.get("text")[1]}Рейтинг блюда: {event.object.payload.get("rat")}',
                conversation_message_id=event.object.conversation_message_id,
                keyboard=create_keyb_3(event.object.payload.get("boon")+1,event.object.payload.get("text"),event.object.payload.get("rat"),event.object.payload.get("name")).get_keyboard())

        elif event.object.payload.get("keyb_3") == 2:
            last_id = vk.messages.edit(
                peer_id = event.object.peer_id,
                attachment = event.object.payload.get("text")[0],
                message = f'{event.object.payload.get("text")[1]}Рейтинг блюда: {event.object.payload.get("rat")}',
                conversation_message_id=event.object.conversation_message_id,
                keyboard=create_keyb_3(event.object.payload.get("boon")-1,event.object.payload.get("text"),event.object.payload.get("rat"),event.object.payload.get("name")).get_keyboard())

        elif event.object.payload.get("keyb_3") == 6:
            dish(event.object.payload.get("keyb_3_dish"), 1)

        elif event.object.payload.get("keyb_3") == 4:
            spis = []
            id_dish = con.execute(f"SELECT id FROM DISHES WHERE name = '{event.object.payload.get('name')}' ").fetchone()
            id_user = con.execute(f"SELECT id FROM USERS WHERE id_vk = {event.object.peer_id} ").fetchone()
            kil_vo = event.object.payload.get("boon")
            max_data = con.execute(
                f"SELECT MAX(date) FROM ORDERS WHERE user = {id_user[0]} ").fetchone()
            id_order = con.execute(
                f"SELECT id FROM ORDERS WHERE user = {id_user[0]} and date = {max_data[0]}").fetchone()
            spis.append(id_dish[0])
            spis.append(kil_vo)
            spis.append(id_order[0])
            with con:
                con.execute(f"INSERT OR IGNORE INTO GOODS (dishes,kol_vo_dishes,orders) values(?,?,?)", spis)
            vk.messages.edit(
                peer_id = event.object.peer_id,
                conversation_message_id=event.object.conversation_message_id,
                message="Блюдо добавлено")

        elif event.object.payload.get("keyb_5") == 1:
            vk.messages.edit(
                peer_id=event.object.peer_id,
                conversation_message_id=event.object.conversation_message_id,
                message="Выберите блюдо",
                keyboard=create_keyb_6(event.object.payload.get("order")).get_keyboard())











if __name__ == '__main__':
    print()