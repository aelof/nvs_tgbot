import telebot
from config import TOKEN
from keyboards import (general_markup, geo_markup, kush_markup,
                       kush_house_markup, menu_markup)
from helpers import hello, State, category_list

bot = telebot.TeleBot(TOKEN,
                      parse_mode='HTML')  # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=['start', 'sendtoall'])
def send_welcome(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    if message.text == '/start':
        bot.send_message(chat_id,
                         'Здравствуйте, ' + str(name) + hello,
                         reply_markup=menu_markup)
    elif message.text == '/sendtoall':
        msg = bot.send_message(chat_id,
                               'Отправьте мне то, что хотите разослать другим')
        bot.register_next_step_handler(msg, sendtoall)

def sendtoall(message):
    try:
        chat_id = message.chat.id
        bot.send_message(chat_id,
                         'Ваше сообщение отправлено всем пользователям бота')
    except Exception as e:
        bot.send_message(chat_id,
                         'Что-то пошло не так, попробуйте заново',
                         reply_markup=general_markup)

@bot.message_handler(func=lambda query: query.text == 'Найти объект')
def search_obj(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Хорошо 👌\nсейчас я помогу подобрать Вам объект\
                            \nвыберете, что Вас интересует',
                     reply_markup=general_markup)


@bot.message_handler(func=lambda query: query.text in category_list)
def investment(message):
    State.category = message.text
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,
                           'Давайте выберем город:',
                           reply_markup=geo_markup)
    bot.register_next_step_handler(msg, choice_geo)


def choice_geo(message):
        chat_id = message.chat.id
        text = message.text
        State.geo = text
        if text in ['Геленджик', 'Анапа', 'Лаго-Наки']:
            msg = bot.send_message(chat_id,
                                   'Давайте выберем бюджет:',
                                   reply_markup=kush_house_markup)
            bot.register_next_step_handler(msg, choice_kush)


def choice_kush(message):
    try:
        chat_id = message.chat.id
        text = message.text
        State.kush = text
        if text in ['5 - 7 млн', '7 - 10 млн', '10+ млн']:
            bot.send_message(
                chat_id,
                f'{State.category}{State.geo}{State.kush}')
            bot.send_message(
                chat_id,
                'Отправляется ссылка из ЦРМ по домам согласно городу и бюджету',
                reply_markup=general_markup)

    except Exception as e:
        bot.send_message(chat_id,
                         'Что-то пошло не так, попробуйте заново',
                         reply_markup=general_markup)


@bot.message_handler(content_types=['text'])
def investment(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,
                           'Что-то пошло не так, попробуйте заново',
                           reply_markup=general_markup)


bot.infinity_polling(interval=0, timeout=20)
