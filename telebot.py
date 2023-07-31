import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto


bot = telebot.TeleBot('6673879527:AAGKIM0bC1Aqqk2uhKkx5w71Yupa2WBYYhg');
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,"Выбери товар и дай много деняк")