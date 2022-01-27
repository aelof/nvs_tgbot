import telebot
from config import TOKEN
from keyboards import (general_markup, geo_markup, kush_markup,
                       kush_house_markup, menu_markup, phone_markup)
from helpers import hello
import dbworker
from helpers import States, Target
from helpers import add_to_db, get_ids

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

category_list = ['Инвестиции', 'Земельные участки', 'Дома', 'Видео обзоры']
menu_list = ['Контакты', 'Заказать звонок', 'Помощь']
back_list = ['↩ Назад', '× Отмена']

# handler for test
@bot.message_handler(commands=['test'])
def cmd_start(msg):
    bot.send_message(msg.chat.id, f'{msg.chat.id}, {msg.from_user.id}')


@bot.message_handler(commands=['start', 'sendtoall'])
def cmd_start(msg):
    if msg.text == '/sendtoall':
        target_msg = bot.send_message(msg.chat.id, ' Отправьте то, что нужно разослать другим:')
        bot.register_next_step_handler(target_msg, send_to_all)
    else:    
        bot.send_message(
        msg.chat.id, f'Здравствуйте, {msg.from_user.first_name} {hello}', reply_markup=menu_markup)
        us_id = msg.from_user.id
        us_firstname = msg.from_user.first_name
        us_username = msg.from_user.username
        us_date = msg.date
        add_to_db(user_id=us_id, firstname = us_firstname, username=us_username, date=us_date)
    

def send_to_all(msg):
    for chat_id in get_ids():
        try:
            bot.send_message(chat_id, msg.text )
        except Exception as e:
            bot.send_message(msg.chat.id, f'пользователь {chat_id} заблокировал бота')



@bot.message_handler(func=lambda msg: msg.text in menu_list)
def search_obj(msg):
    if msg.text == 'Контакты':
        bot.send_message(msg.chat.id, 'Отправка блока контактов')
    elif msg.text == 'Помощь':
        bot.send_message(msg.chat.id, 'Отправка блока c помощью')
    elif msg.text == 'Заказать звонок':
        bot.send_message(
            msg.chat.id, 'Нажмите кнопку поделиться на клавиатуре', reply_markup=phone_markup)


# return to main menu or cancel to share phone number
@bot.message_handler(func=lambda msg: msg.text in back_list)
def back(msg):
    if msg.text == '↩ Назад':
        bot.send_message(
            msg.chat.id, "Вы вернулись в начальное меню выбора объекта", reply_markup=general_markup)
        dbworker.set_state(msg.chat.id, States.ENTER_CAT.value)
    else:
        bot.send_message(
            msg.chat.id, "Вы вернулись в главное меню", reply_markup=menu_markup)


@bot.message_handler(func=lambda msg: msg.text == 'Найти объект')
def search_obj(msg):
    bot.send_message(msg.chat.id,
                     'Хорошо 👌\nсейчас я помогу подобрать Вам объект\
                            \nвыберете, что Вас интересует',
                     reply_markup=general_markup)
    dbworker.set_state(msg.chat.id, States.ENTER_CAT.value)


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.ENTER_CAT.value)
def investment(msg):
    chat_id = msg.chat.id
    bot.send_message(chat_id,
                     'Давайте выберем город:', reply_markup=geo_markup)
    dbworker.set_state(msg.chat.id, States.ENTER_GEO.value)
    Target.add_to_query(msg.text)


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.ENTER_GEO.value)
def entering_kush(msg):
    if msg.text in ['Геленджик', 'Анапа', 'Лаго-Наки']:
        Target.add_to_query(msg.text)
        if Target.show_query()[0] == 'Дома':
            bot.send_message(
                msg.chat.id, "Хорошо! Последний шаг - бюджет!", reply_markup=kush_house_markup)
        else:
            bot.send_message(
                msg.chat.id, "Хорошо! Последний шаг - бюджет!", reply_markup=kush_markup)
        dbworker.set_state(msg.chat.id, States.ENTER_KUSH.value)


@bot.message_handler(func=lambda msg: dbworker.get_current_state(msg.chat.id) == States.ENTER_KUSH.value)
def final(msg):
    Target.add_to_query(msg.text)
    bot.send_message(msg.chat.id, 'Отправляется ссылка из ЦРМ по запросу:')
    bot.send_message(msg.chat.id, str(Target.show_query()))
    Target.clear_query()
    bot.send_message(
        msg.chat.id, '<i>Для удобства Вы перенеправлены в главное меню</i>', reply_markup=menu_markup)


@bot.message_handler(content_types=['text'])
def investment(msg):
    chat_id = msg.chat.id
    msg = bot.send_message(chat_id,
                           'Что-то пошло не так, попробуйте заново',
                           reply_markup=general_markup)


@bot.message_handler(content_types=['contact'])
def investment(msg):
    number = msg.contact.phone_number
    bot.send_message(
        msg.chat.id, f'Отправка контакта оператору  {msg.from_user.first_name} {number}')
    bot.send_message(msg.chat.id, '<i>Переход в главное меню</i>',
                     reply_markup=menu_markup)





bot.infinity_polling(interval=0, timeout=20)
