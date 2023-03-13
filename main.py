import telebot
from telebot import types
from requests.exceptions import ReadTimeout
from datetime import datetime, timedelta
from random import randrange


bot = telebot.TeleBot('ENTER_YOUR_TOKEN')


VALID_ID = 'ENTER_YOUR_ID'
NEXT_MSG_DATE = False
NEXT_MSG_MSG = False
SUB = ['A', 'P']
DATERANGE = '01.01.00-31.12.30'
MSG = 'Дмитрий поел пиццу в \"\". Примерно в \'\'.'


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def prepareMessage():
    global MSG
    global DATERANGE
    parsed = parseDate(DATERANGE)
    date = random_date(parsed[0], parsed[1])
    new_msg = MSG.replace('\"\"', f'{date.day}.{date.month}.{date.year}')
    new_msg = new_msg.replace('\'\'', f'{date.hour}:{date.minute}')
    return new_msg


def parseDate(s):
    start = datetime.strptime(f'{s[:2]}.{s[3:5]}.20{s[6:8]} {int(randrange(1, 12))}:'
                              f'{int(randrange(0, 60))} {SUB[randrange(0, 2)]}M', '%d.%m.%Y %I:%M %p')
    end = datetime.strptime(f'{s[9:11]}.{s[12:14]}.20{s[15:17]} {int(randrange(1, 12))}:'
                            f'{int(randrange(0, 60))} {SUB[randrange(0, 2)]}M', '%d.%m.%Y %I:%M %p')
    return start, end


def setBaseMarkups():
    dt = types.KeyboardButton('Задать дату')
    msg = types.KeyboardButton('Задать сообщение')
    run = types.KeyboardButton('Запустить генерацию')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(dt, msg, run)
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


@bot.message_handler(content_types=['text'])
def func(message):
    global NEXT_MSG_MSG
    global NEXT_MSG_DATE
    global DATERANGE
    global MSG
    global VALID_ID
    if int(message.chat.id) != VALID_ID:
        mess = f'Привет, <b>{message.from_user.first_name}</b>, к сожалению, у вас нет прав'
        bot.send_message(message.chat.id, mess, parse_mode='html')
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
        # while True:
        for i in range(10):
            mess = prepareMessage()
            bot.send_message(message.chat.id, mess, parse_mode='html')


try:
    bot.polling(none_stop=True)
except ReadTimeout:
    pass
