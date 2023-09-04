from vk_api import VkApi
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3 as sl
import json
import array

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
    markup1 = VkKeyboard(**settings)
    markup1.add_button(label='Регистрация 👋', color=VkKeyboardColor.NEGATIVE, payload={"type": "text"})
    markup1.add_line()
    markup1.add_button(label='Проверить регистрацию', color=VkKeyboardColor.POSITIVE, payload={"type": "text"})
    return markup1

def create_keyboard_2():
    markup2 = VkKeyboard(**settings)
    markup2.add_button(label="📜Меню", color=VkKeyboardColor.PRIMARY, payload={"type": "text"})
    markup2.add_line()
    markup2.add_button(label="🛒Корзина", color=VkKeyboardColor.PRIMARY, payload={"type": "text"})
    markup2.add_line()
    markup2.add_button(label="❓Поддержка ", color=VkKeyboardColor.PRIMARY, payload={"type": "text"})
    markup2.add_line()
    markup2.add_button(label="📒Мои заказы ", color=VkKeyboardColor.PRIMARY, payload={"type": "text"})
    return markup2

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

def create_keyb_3(boon):

    keyb = VkKeyboard(**settings2)
    keyb.add_callback_button(label="➖", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 2})
    keyb.add_callback_button(label=f"{str(boon+boon)}", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 5})
    keyb.add_callback_button(label="➕", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 1})
    keyb.add_line()
    keyb.add_callback_button(label="Заказать 📒", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 3})
    keyb.add_callback_button(label="Добавить в корзину 🛒", color=VkKeyboardColor.PRIMARY, payload={"keyb_3": 4})
    keyb.add_line()
    keyb.add_callback_button(label="Следующее блюдо ➡️", color=VkKeyboardColor.PRIMARY, payload={"keyb_3":6})
    return keyb


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

def dish(objec):
    a = []
    sr = ""
    dish_id = con.execute(f"SELECT id FROM DISHES WHERE stoped={0} AND name ='{objec.object.payload.get('dish')}'").fetchone()
    rating = con.execute(f"SELECT rating FROM rating WHERE dish = {int(dish_id[0])}").fetchone()
    for x in range(len(rating)):
        a.append(rating[x])
    rating_list = (4 + int(sum(a))) / len(rating)
    with con:
        con.execute(f"UPDATE DISHES SET rating = {int(rating_list)} WHERE id = {int(dish_id[0])}")
    dish = con.execute(f"SELECT id,photo,name,weight,description,price,rating FROM DISHES WHERE stoped={0} AND name ='{objec.object.payload.get('dish')}'").fetchone()

    photo = vk_upload.photo_messages(f"C:/Users/ReDWaR/PycharmProjects/pythonProject_telebot/photo/{dish[1]}.png")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    for a in dish[2:6]:
        sr += f'{str(a)}\n'
    last_id = vk.messages.edit(
        attachment=attachment,
        peer_id=objec.obj.peer_id,
        message=f'{sr}Рейтинг блюда: {dish[6]}',
        conversation_message_id=objec.obj.conversation_message_id,
        keyboard=create_keyb_3(1).get_keyboard())


#Смена id пользователя
def change_id_user(phone,obj):
    print(phone)
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
                        message="Введите свой адрес доставки начиная с ул.")

                elif "ул." in event.obj.message['text']:
                    try:
                        users.append(event.obj.message['text'])
                        con = sl.connect('tgbase.db')
                        with con:
                            con.execute("INSERT OR IGNORE INTO USERS (id_vk,name,tel,address) values(?, ?, ?, ?)", users)
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
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        message="Дарова корова")
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
            dish(event)
        elif event.object.payload.get("keyb_3") == 1:
            create_keyb_3(1)
            # last_id = vk.messages.edit(
            #     peer_id=event.obj.peer_id,
            #     message = 'h',
            #     conversation_message_id=event.obj.conversation_message_id,
            #     keyboard=create_keyb_3(1).get_keyboard())





if __name__ == '__main__':
    print()