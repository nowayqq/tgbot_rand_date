import telebot
from telebot import types
from requests.exceptions import ReadTimeout
from datetime import datetime, timedelta
from random import randrange
import time


bot = telebot.TeleBot('')


VALID_ID =
NEXT_MSG_DATE = False
NEXT_MSG_MSG = False
DATERANGE = '01.01.00-31.12.30'
MSG = 'Дмитрий поел пиццу в \"\". Примерно в \'\'.'
START = None
END = None
BRAKEFLAG = False


def prepareMessage():
    global MSG
    global DATERANGE
    global START
    START += timedelta(hours=1)
    new_msg = MSG.replace('\"\"', f'{START.day}.{START.month}.{START.year}')
    new_msg = new_msg.replace('\'\'', f'{START.hour}:00')
    return new_msg


def parseDate(s):
    start_ = datetime.strptime(f'{s[:2]}.{s[3:5]}.20{s[6:8]} {int(randrange(1, 12))}:'
                               f'{int(randrange(0, 60))} AM', '%d.%m.%Y %I:%M %p')
    end_ = datetime.strptime(f'{s[9:11]}.{s[12:14]}.20{s[15:17]} {int(randrange(1, 12))}:'
                             f'{int(randrange(0, 60))} AM', '%d.%m.%Y %I:%M %p')
    global START
    global END
    START = start_
    END = end_


def setBaseMarkups():
    dt = types.KeyboardButton('Задать дату')
    msg = types.KeyboardButton('Задать сообщение')
    run = types.KeyboardButton('Запустить генерацию')
    st = types.KeyboardButton('/stop')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(dt, msg, run, st)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    global VALID_ID
    if int(message.chat.id) != VALID_ID:
        mess = f'Привет, <b>{message.from_user.first_name}</b>, к сожалению, у вас нет прав'
        bot.send_message(message.chat.id, mess, parse_mode='html')
    else:
        mess = f'Привет, <b>{message.from_user.first_name}</b>'
        markup = setBaseMarkups()
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    print(message.chat.id)


@bot.message_handler(commands=['stop'])
def stop(message):
    global VALID_ID
    if int(message.chat.id) != VALID_ID:
        mess = f'Привет, <b>{message.from_user.first_name}</b>, к сожалению, у вас нет прав'
        bot.send_message(message.chat.id, mess, parse_mode='html')
    else:
        mess = f'Остановка'
        markup = setBaseMarkups()
        global BRAKEFLAG
        BRAKEFLAG = True
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    print(message.chat.id)


@bot.message_handler(content_types=['text'])
def func(message):
    global NEXT_MSG_MSG
    global NEXT_MSG_DATE
    global DATERANGE
    global MSG
    global VALID_ID

    if int(message.chat.id) != VALID_ID:
        mess = f'Привет, <b>{message.from_user.first_name}</b>, к сожалению, у вас нет прав'
        bot.send_message(, mess, parse_mode='html')
    elif NEXT_MSG_DATE:
        NEXT_MSG_DATE = False
        DATERANGE = message.text
    elif NEXT_MSG_MSG:
        NEXT_MSG_MSG = False
        MSG = message.text
    elif message.text == 'Задать дату':
        NEXT_MSG_DATE = True
    elif message.text == 'Задать сообщение':
        NEXT_MSG_MSG = True
    elif message.text == 'Запустить генерацию':
        parseDate(DATERANGE)
        global START
        global END
        global BRAKEFLAG
        BRAKEFLAG = False
        bot.send_message(message.chat.id, 'Запускаю', parse_mode='html')
        i = 0
        while True:
            if START == END or BRAKEFLAG:
                break
            if not i % 5:
                time.sleep(1)
            mess = prepareMessage()
            bot.send_message(, mess, parse_mode='html')


try:
    bot.polling(none_stop=True)
except ReadTimeout:
    pass
