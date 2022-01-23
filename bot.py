import telebot
from config import TOKEN
from keyboards import (general_markup, geo_markup, kush_markup,
                       kush_house_markup, menu_markup)
from helpers import hello, category_list
import dbworker
from helpers import States

bot = telebot.TeleBot(TOKEN,
                      parse_mode='HTML')  # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=['start', 'sendtoall'])
def cmd_start(message):
    bot.send_message(message.chat.id, "Хорошо, давайте выберем то, что Вас интересует:", reply_markup=menu_markup)
    dbworker.set_state(message.chat.id, States.ENTER_CAT.value)

@bot.message_handler(func=lambda message: message.text == '↩ Назад')
def back(message):
        bot.send_message(message.chat.id, "Вы вернулись в начальное меню выбора объекта", reply_markup=menu_markup)
        dbworker.set_state(message.chat.id, States.ENTER_CAT.value)


@bot.message_handler(func=lambda query: query.text == 'Найти объект')
def search_obj(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Хорошо 👌\nсейчас я помогу подобрать Вам объект\
                            \nвыберете, что Вас интересует',
                     reply_markup=general_markup)
    dbworker.set_state(message.chat.id, States.ENTER_CAT.value)




@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == States.ENTER_CAT.value)
def investment(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                           'Давайте выберем город:', reply_markup=geo_markup)
    dbworker.set_state(message.chat.id, States.ENTER_GEO.value)




@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == States.ENTER_GEO.value)
def user_entering_age(message):
    if message.text in ['Геленджик', 'Анапа', 'Лаго-Наки']:
        bot.send_message(message.chat.id, "Хорошо! Последний шаг - бюджет!", reply_markup=kush_markup)
        dbworker.set_state(message.chat.id, States.ENTER_KUSH.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == States.ENTER_KUSH.value)
def enter_kush(message):
    bot.send_message(message.chat.id, 'Отправляется ссылка из ЦРМ', reply_markup=menu_markup)


@bot.message_handler(content_types=['text'])
def investment(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,
                           'Что-то пошло не так, попробуйте заново',
                           reply_markup=general_markup)


bot.infinity_polling(interval=0, timeout=20)
