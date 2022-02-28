import telebot
from config import TOKEN
import dbworker
import logging, os 
from datetime import datetime
from helpers import States, Target, User, db_insert_user_request, exist_name, exist_request, get_name, sql_to_csv, admin_help
from helpers import exist_phone, db_insert_user_info, get_ids, db_get_link, db_insert_phone, get_phone
from helpers import hello, help, contacts, category_list, menu_list, back_list, kush_list, teh_channel
from keyboards import (general_markup, geo_markup, kush_markup,
                       kush_house_markup, menu_markup, phone_markup,
                       hide_markup, yt_markup, order_call_kb)


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
# telebot.logger.setLevel(logging.DEBUG)


bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# handler for test


@bot.message_handler(commands=['test'])
def cmd_start(msg):
    if msg.from_user.id == 239090651:
        bot.send_message(teh_channel, f'{msg.chat.id}, {msg.from_user.id}')


# first touch with user
@bot.message_handler(commands=['start'])
def first_message(msg):
    Target.clear_query()
    id = msg.from_user.id
    if get_name(id):
        bot.send_message(id,
                         f'И снова здравствуйте, {get_name(id)}! \nПеренаправляю Вас в главное меню',
                         reply_markup=menu_markup)
    else:
        bot.send_message(
            msg.chat.id, f'Здравствуйте{hello}', reply_markup=hide_markup)
        bot.send_message(msg.chat.id, 'А как Вас зовут ? ')
        bot.send_message(msg.chat.id,
                         '<i>Введите Ваше имя в текстовое поле, перед отправкой <b>убедитесь в правильности</b></i>')
        dbworker.set_state(msg.chat.id, States.NAME.value)


# after enter name
@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.NAME.value)
def entering_kush(msg):
    bot.send_message(msg.chat.id, f'Рад знакомству, {msg.text}!')
    bot.send_message(msg.chat.id,
                     f'Перенаправляю Вас в главное меню\n'
                     '\nЕсли Вам ранее не приходилось работать с чат-ботами, нажмите "Помощь" на клавиатуре',
                      reply_markup=menu_markup)

    dbworker.set_state(msg.from_user.id, States.MENU.value)

    name = msg.text
    user_id = msg.from_user.id
    user_firstname = msg.from_user.first_name
    user_username = msg.from_user.username
    user_date = datetime.utcfromtimestamp(msg.date).strftime('%y-%m-%d')
    db_insert_user_info(name=name,
                        user_id=user_id,
                        firstname=user_firstname,
                        username=user_username,
                        reg_date=user_date)


# handler for custom commands
@bot.message_handler(commands=['admin', 'exportdb', 'sendtoall'])
def admin_message(msg):
    if msg.text == '/admin':
        bot.send_message(msg.chat.id, admin_help)
    if msg.text == '/sendtoall':
        bot.send_message(msg.chat.id, 'этот раздел ещё дорабатывается')
    if msg.text == '/exportdb':
        if sql_to_csv():
            path_to_db = os.getcwd() + '/Users.csv'
            f = open(path_to_db,"rb")
            bot.send_document(msg.chat.id, document=f)
        else: 
            bot.send_message(msg.chat.id, 'Произошла ошибка, напишите @alexpure')


# def send_to_all(msg):
#     for chat_id in get_ids():
#         try:
#             bot.send_message(chat_id, msg.text)
#         except Exception as e:
#             bot.send_message(
#                 msg.chat.id, f'пользователь {chat_id} заблокировал бота')


@bot.message_handler(func=lambda msg: msg.text in menu_list)
def search_obj(msg):
    if msg.text == 'Контакты':
        bot.send_message(
            msg.chat.id, contacts) 
    elif msg.text == 'Помощь':
        bot.send_message(
            msg.chat.id, help)
    elif msg.text == 'Видео обзоры':
        bot.send_message(
            msg.chat.id, 'Вот, пожалуйста: ', reply_markup=yt_markup)
    elif msg.text == 'Заказать звонок':
        if exist_phone(msg.chat.id):
            bot.send_message(msg.chat.id, 'Вы уверены?',
                             reply_markup=order_call_kb)
            dbworker.set_state(msg.chat.id, States.ORDER_CALL.value)
        else:
            bot.send_message(
                msg.chat.id, 'Нажмите кнопку поделиться на клавиатуре', reply_markup=phone_markup)


# return to main menu or cancel to share phone number
@bot.message_handler(func=lambda msg: msg.text in back_list)
def back(msg):
    if msg.text == '↩ Назад':
        bot.send_message(msg.chat.id,
                         "Вы вернулись в начальное меню выбора объекта", reply_markup=geo_markup)
        dbworker.set_state(msg.chat.id, States.GEO.value)
        Target.clear_query()
    elif msg.text == '↩ Главное меню':
        bot.send_message(msg.chat.id,
                         "Вы вернулись в главное меню", reply_markup=menu_markup)
        # dbworker.set_state(msg.chat.id, States.CAT.value)
    else:
        bot.send_message(
            msg.chat.id, "Вы вернулись в главное меню", reply_markup=menu_markup)


@bot.message_handler(func=lambda msg: msg.text == 'Найти объект')
def search_obj(msg):
    bot.send_message(msg.chat.id,
                     'Хорошо 👌\nсейчас я помогу подобрать Вам объект\
                            \nвыберете локацию:',
                     reply_markup=geo_markup)
    dbworker.set_state(msg.chat.id, States.GEO.value)


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.GEO.value)
def entering_kush(msg):
    if msg.text in ['Геленджик', 'Анапа', 'Лаго-Наки']:
        Target.add_to_query(msg.text)
        bot.send_message(msg.chat.id,
                         "С локацией определились! Теперь давайте выберем что Вас интересует", reply_markup=general_markup)
        dbworker.set_state(msg.chat.id, States.CAT.value)
    else:
        bot.send_message(msg.chat.id,
                         "Выберете доступный вариант из меню ниже")


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.CAT.value)
def investment(msg):
    Target.add_to_query(msg.text)
    if msg.text in category_list:
        if Target.show_query()[1] == 'Дома':
            bot.send_message(msg.chat.id,
                             'А теперь давайте выберем бюджет', reply_markup=kush_house_markup)
        else:
            bot.send_message(msg.chat.id,
                             'А теперь давайте выберем бюджет', reply_markup=kush_markup)
        dbworker.set_state(msg.chat.id, States.KUSH.value)
    else:
        bot.send_message(msg.chat.id, 'На клавиатуре такого не было!')


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.KUSH.value)
def before_final(msg):
    if msg.text in kush_list:
        Target.add_to_query(msg.text)
        if exist_phone(msg.chat.id):
            bot.send_message(msg.chat.id, db_get_link(*Target.show_query()))
            bot.send_message(
                msg.chat.id, f'{get_name(msg.chat.id)}, ☝️ вот ваша индивидуальная подборка')
            bot.send_message(msg.chat.id,
                             '<i>Для удобства Вы перенеправлены в главное меню</i>',
                             reply_markup=menu_markup, disable_notification=True)
            if exist_request(msg.chat.id):
                pass
            else:
                db_insert_user_request(msg.chat.id, str(Target.show_query()) )
            Target.clear_query()

        else:
            bot.send_message(
                msg.chat.id, 'Чтобы получить подборку - поделитесь своим номером телефона', reply_markup=phone_markup)
            dbworker.set_state(msg.chat.id, States.PHONE.value)


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.ORDER_CALL.value)
def order_call(msg):
    if msg.text == "Да, заказать":
        bot.send_message(
            msg.chat.id, f'Хоршо, {get_name(msg.chat.id)} cкоро с Вами свяжется специалист')
        bot.send_message(msg.chat.id, '<i>Перенаправляю в главное меню</i>',
                         reply_markup=menu_markup, disable_notification=True)
        bot.send_message(
            teh_channel, f'Новый заказ обратного звонка:\n{get_phone(msg.chat.id)}')


@bot.message_handler(content_types=['contact'])
def handle_contact(msg):
    phone = msg.contact.phone_number
    if dbworker.get_current_state(msg.from_user.id) == States.PHONE.value:
        phone = msg.contact.phone_number
        bot.send_message(msg.chat.id, db_get_link(*Target.show_query()))
        bot.send_message(
            msg.chat.id, f'{get_name(msg.chat.id)}, ☝️ вот ваша индивидуальная подборка')
        bot.send_message(msg.chat.id,
                         '<i>Для удобства Вы перенеправлены в главное меню</i>',
                         reply_markup=menu_markup,  disable_notification=True)
        if exist_request(msg.chat.id):
            pass
        else:
            db_insert_user_request(msg.chat.id, str(Target.show_query()) )
        Target.clear_query()

    else:
        bot.send_message(msg.chat.id,
                         'Оператор с Вами свяжется в ближайшее время, благодарим за обращение !')
        bot.send_message(
            teh_channel, f'Новый заказ обратного звонка:\n{phone}')
        bot.send_message(msg.chat.id, '<i>Перенаправляю в главное меню</i>',
                         reply_markup=menu_markup, disable_notification=True)

    if exist_phone(msg.from_user.id):
        pass
    else:
        db_insert_phone(msg.from_user.id, phone)


@bot.message_handler(content_types=['text'])
def investment(msg):    msg = bot.send_message(msg.chat.id,
                           'Что-то пошло не так, попробуйте перезагрузить командой  /start',
                           reply_markup=general_markup)


bot.infinity_polling(timeout=18, skip_pending=True)
