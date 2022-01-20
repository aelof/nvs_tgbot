import telebot
from config import TOKEN
from keyboards import (general_markup, geo_markup, kush_markup,
                       kush_house_markup, phone_markup, hello)

bot = telebot.TeleBot(
    TOKEN,
    parse_mode='HTML')  # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=['start', 'sendtoall'])
def send_welcome(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    if message.text == '/start':
        bot.send_message(chat_id,
                     'Здравствуйте, ' + str(name) + hello,
                     reply_markup=general_markup)
    elif message.text == '/sendtoall':
        msg = bot.send_message(chat_id,
                           'Отправьте мне то, что хотите разослать другим')
        bot.register_next_step_handler(msg, sendtoall)


def sendtoall(message):
    try:
        chat_id = message.chat.id
        text = message.text
        bot.send_message(chat_id,
                         'Ваше сообщение отправлено всем пользователям бота')
    except Exception as e:
        bot.send_message(chat_id,
                         'Что-то пошло не так, попробуйте заново',
                         reply_markup=general_markup)


@bot.message_handler(func=lambda query: query.text == 'Инвестиции')
def investment(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,
                           'Давайте выберем город:',
                           reply_markup=geo_markup)
    bot.register_next_step_handler(msg, choice_geo)


@bot.message_handler(func=lambda query: query.text == 'Земельные участки')
def investment(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,
                           'Давайте выберем город:',
                           reply_markup=geo_markup)
    bot.register_next_step_handler(msg, choice_geo)


@bot.message_handler(func=lambda query: query.text == 'Дома')
def investment(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,
                           'Давайте выберем город:',
                           reply_markup=geo_markup)
    bot.register_next_step_handler(msg, choice_geo_house)


@bot.message_handler(func=lambda query: query.text == 'Видео обзоры')
def investment(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,
                           'Давайте выберем город:',
                           reply_markup=geo_markup)
    bot.register_next_step_handler(msg, choice_geo_video)


def choice_geo_house(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text == 'Геленджик':
            msg = bot.send_message(chat_id,
                                   'Давайте выберем бюджет:',
                                   reply_markup=kush_house_markup)
            bot.register_next_step_handler(msg, choice_kush_house)
        elif text == 'Анапа':
            msg = bot.send_message(chat_id,
                                   'Давайте выберем бюджет:',
                                   reply_markup=kush_house_markup)
            bot.register_next_step_handler(msg, choice_kush_house)
        elif text == 'Лаго-Наки':
            msg = bot.send_message(chat_id,
                                   'Давайте выберем бюджет:',
                                   reply_markup=kush_house_markup)
            bot.register_next_step_handler(msg, choice_kush_house)
    except Exception as e:
        bot.send_message(chat_id,
                         'Что-то пошло не так, попробуйте заново',
                         reply_markup=general_markup)


def choice_kush_house(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text in ['5 - 7 млн', '7 - 10 млн', '10+ млн']:
            bot.send_message(
                chat_id,
                'Отправляется ссылка из ЦРМ по домам согласно городу и бюджету',
                reply_markup=general_markup)
    except Exception as e:
        bot.send_message(chat_id,
                         'Что-то пошло не так, попробуйте заново',
                         reply_markup=general_markup)


def choice_geo(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text == 'Геленджик':
            msg = bot.send_message(chat_id,
                                   'Давайте выберем бюджет:',
                                   reply_markup=kush_markup)
            bot.register_next_step_handler(msg, choice_kush)
        elif text == 'Анапа':
            msg = bot.send_message(chat_id,
                                   'Давайте выберем бюджет:',
                                   reply_markup=kush_markup)
            bot.register_next_step_handler(msg, choice_kush)
        elif text == 'Лаго-Наки':
            msg = bot.send_message(chat_id,
                                   'Давайте выберем бюджет:',
                                   reply_markup=kush_markup)
            bot.register_next_step_handler(msg, choice_kush)
        else:
            bot.send_message(chat_id,
                             'Что-то пошло не так, попробуйте заново',
                             reply_markup=general_markup)
    except Exception as e:
        bot.send_message(chat_id,
                         'Что-то пошло не так, попробуйте заново',
                         reply_markup=general_markup)


def choice_geo_video(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text in ['Геленджик', 'Анапа', 'Лаго-Наки']:
            bot.send_message(chat_id,
                             'Отправляется ссылка на плейлист ютьюб',
                             reply_markup=general_markup)
    except Exception as e:
        bot.send_message(chat_id,
                         'Что-то пошло не так, попробуйте заново',
                         reply_markup=general_markup)


def choice_kush(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text in ['до 1 млн', '1 - 3 млн', '3+ млн']:
            bot.send_message(
                chat_id,
                'Отправляется ссылка из ЦРМ согласно городу и бюджету',
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

# def choice_geo(message):
#     try:
#         chat_id = message.chat.id
#         text = message.text
#         if text in ['Геленджик', 'Анапа', 'Лаго-Наки']:
#             msg = bot.send_message(chat_id, 'Давайте выберем бюджет:', reply_markup=kush_markup)
#             bot.register_next_step_handler(msg, choice_kush)
#     except Exception as e:
#         bot.reply_to(message, 'Что-то пошло не так, попробуйте заново через команду /start')