import telebot
from config import TOKEN
import dbworker
import logging
from helpers import States, Target, hello, add_to_db, get_ids, add_phone_to_db, get_link
from keyboards import (general_markup, geo_markup, kush_markup,
                       kush_house_markup, menu_markup, phone_markup)


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
# telebot.logger.setLevel(logging.DEBUG)


# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

category_list = ['Инвестиции', 'Земельные участки', 'Дома', ]
menu_list = ['Контакты', 'Заказать звонок', 'Помощь', 'Видео обзоры']
back_list = ['↩ Назад', '× Отмена', '↩ Главное меню']
kush_list = ['до 1 млн', '1 - 3 млн', '3+ млн',
             '5 - 7 млн', '7 - 10 млн', '10+ млн']
teh_channel = -1001511156970


# handler for test
@bot.message_handler(commands=['test'])
def cmd_start(msg):
    if msg.from_user.id == 239090651:
        bot.send_message(teh_channel, f'{msg.chat.id}, {msg.from_user.id}')


@bot.message_handler(commands=['start', 'sendtoall'])
def cmd_start(msg):
    Target.clear_query()
    if msg.text == '/sendtoall':
        target_msg = bot.send_message(
            msg.chat.id, ' Отправьте то, что нужно разослать другим:')
        bot.register_next_step_handler(target_msg, send_to_all)
    else:
        bot.send_message(
            msg.chat.id, f'Здравствуйте{hello}', reply_markup=menu_markup)
        us_id = msg.from_user.id
        us_firstname = msg.from_user.first_name
        us_username = msg.from_user.username
        us_date = msg.date
        add_to_db(user_id=us_id, firstname=us_firstname,
                  username=us_username, date=us_date)


def send_to_all(msg):
    for chat_id in get_ids():
        try:
            bot.send_message(chat_id, msg.text)
        except Exception as e:
            bot.send_message(
                msg.chat.id, f'пользователь {chat_id} заблокировал бота')


@bot.message_handler(func=lambda msg: msg.text in menu_list)
def search_obj(msg):
    if msg.text == 'Контакты':
        bot.send_message(
            msg.chat.id, 'Отправка блока контактов со всеми номерами и социальными сетями компании')
    elif msg.text == 'Помощь':
        bot.send_message(
            msg.chat.id, 'Отправка блока c помощью(краткая информация о том, как извлечь максимальную пользу от бота)')
    elif msg.text == 'Видео обзоры':
        bot.send_message(
            msg.chat.id, 'its still empty')
    elif msg.text == 'Заказать звонок':
        bot.send_message(
            msg.chat.id, 'Нажмите кнопку поделиться на клавиатуре', reply_markup=phone_markup)


# return to main menu or cancel to share phone number
@bot.message_handler(func=lambda msg: msg.text in back_list)
def back(msg):
    if msg.text == '↩ Назад':
        bot.send_message(msg.chat.id,
                         "Вы вернулись в начальное меню выбора объекта", reply_markup=geo_markup)
        dbworker.set_state(msg.chat.id, States.ENTER_GEO.value)
        Target.clear_query()
    elif msg.text == '↩ Главное меню':
        bot.send_message(msg.chat.id,
                         "Вы вернулись в главное меню", reply_markup=menu_markup)
        # dbworker.set_state(msg.chat.id, States.ENTER_CAT.value)
    else:
        bot.send_message(
            msg.chat.id, "Вы вернулись в главное меню", reply_markup=menu_markup)


@bot.message_handler(func=lambda msg: msg.text == 'Найти объект')
def search_obj(msg):
    bot.send_message(msg.chat.id,
                     'Хорошо 👌\nсейчас я помогу подобрать Вам объект\
                            \nвыберете локацию:',
                     reply_markup=geo_markup)
    dbworker.set_state(msg.chat.id, States.ENTER_GEO.value)


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.ENTER_GEO.value)
def entering_kush(msg):
    if msg.text in ['Геленджик', 'Анапа', 'Лаго-Наки']:
        Target.add_to_query(msg.text)
        bot.send_message(msg.chat.id,
                         "С локацией определились! Теперь давайте выберем что Вас интересует", reply_markup=general_markup)
        dbworker.set_state(msg.chat.id, States.ENTER_CAT.value)
    else:
        bot.send_message(msg.chat.id,
                         "Выберете доступный вариант из меню ниже")


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.ENTER_CAT.value)
def investment(msg):
    Target.add_to_query(msg.text)
    if msg.text in category_list:
        if Target.show_query()[1] == 'Дома':
            bot.send_message(msg.chat.id,
                             'А теперь давайте выберем бюджет', reply_markup=kush_house_markup)
        else:
            bot.send_message(msg.chat.id,
                             'А теперь давайте выберем бюджет', reply_markup=kush_markup)
        dbworker.set_state(msg.chat.id, States.ENTER_KUSH.value)
    else:
        bot.send_message(msg.chat.id, 'На клавиатуре такого не было!')


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.ENTER_KUSH.value)
def final(msg):
    if msg.text in kush_list:
        Target.add_to_query(msg.text)
        try:
            bot.send_message(msg.chat.id, get_link(*Target.show_query() ) )
            bot.send_message(msg.chat.id, '☝️ вот ваша индивидуальная подборка' )
            bot.send_message(msg.chat.id,
                             '<i>Для удобства Вы перенеправлены в главное меню</i>', reply_markup=menu_markup)
        except:
            bot.send_message(
                msg.chat.id, 'Где-то ошибка, попробуйте перезапустить меня через меню ')

        Target.clear_query()


@bot.message_handler(content_types=['text'])
def investment(msg):
    chat_id = msg.chat.id
    msg = bot.send_message(chat_id,
                           'Что-то пошло не так, попробуйте перезагрузить командой  /start',
                           reply_markup=general_markup)


@bot.message_handler(content_types=['contact'])
def investment(msg):
    phone = msg.contact.phone_number
    bot.send_message(msg.chat.id,
                     'Оператор с Вами свяжется в ближайшее время, благодарим за обращение !')
    bot.send_message(teh_channel, f'Новый заказ обратного звонка:\n{phone}')
    bot.send_message(msg.chat.id, '<i>Переход в главное меню</i>',
                     reply_markup=menu_markup)
    add_phone_to_db(phone, msg.chat.id)


bot.infinity_polling(interval=0, timeout=20)
