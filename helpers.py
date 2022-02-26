from enum import Enum
import sqlite3

# db file to class States
db_file = "database.vdb"


conn = sqlite3.connect('Users.db', check_same_thread=False)
# for output in list format instead tuple
conn.row_factory = lambda cursor, row: row[0]
cursor = conn.cursor()


def db_insert_user_info(name, user_id, firstname, username, reg_date):
    cursor.execute('INSERT INTO Users (name, user_id, firstname, username, reg_date) VALUES (?, ?, ?, ?, ?)',
                   (name, user_id, firstname, username, reg_date))
    conn.commit()


def get_ids():
    cursor.execute('select user_id  from Users')
    return cursor.fetchall()


def db_get_link(where, what, how):
    conn = sqlite3.connect('links.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT Ссылка FROM Sheet1 WHERE Территория=? AND Категория=?  AND Бюджет=?', (where, what, how))
        return cursor.fetchone()
    except:
        return False


def db_insert_phone(user_id, phone):
    cursor.execute(
        f'UPDATE Users SET phone = ? WHERE user_id = ? ', (phone, user_id))
    conn.commit()


def exist_phone(user_id):
    cursor.execute('SELECT phone FROM Users WHERE user_id=user_id')
    if cursor.fetchone():
        return True
    else:
        return False


def exist_name(user_id):
    '''
    Check if name already in DB
    '''
    cursor.execute('SELECT name FROM Users WHERE user_id=user_id')
    if cursor.fetchone():
        return True
    else:
        return False

def get_name(user_id):
    '''
    Just get name from DB
    '''
    cursor.execute('SELECT name FROM Users WHERE user_id=user_id')
    return cursor.fetchone()


class User:
    name = None

    @property
    def from_db_name(user_id):
        pass


class States(Enum):

    NAME = '0'
    MENU = '1'
    GEO = '2'
    CAT = '3'
    KUSH = '4'
    PHONE = '5'


class Target:
    QUERY = []

    def add_to_query(query):
        Target.QUERY.append(query)

    def show_query():
        return Target.QUERY

    def clear_query():
        Target.QUERY.clear()


hello = '''🙋‍♂️
Я - Владимир, Ваш виртуальный помошник компании <a href='https://www.youtube.com/channel/UCRXMqWZwA6bH8DSd6SCOezg'>Новострой</a>!,
Меня придумали для того, чтобы я помог Вам выбрать объекты недвижимости 
'''
'''Общаться мы будем с помощью клавиатуры. Мне так понятнее понимать запрос.\n 
Сейчас Вы в <b>главном меню</b>, ориентируйтесь по кнопкам ниже \n
<i>Если вы не знакомы с работой бота - советуем обратиться за помощью, выбрав "Помощь" на клавиатуре ниже </i>'''

help = ''' В основном вся коммуникация с ботом будет происходить через встроенную клавиатуру\n
Почти всё общение сводиться к ответу на вопросы путём выбора вариантов ответа на клавиатуре снизу\n 
Если вдруг бот перестал отвечать или сообщает об ошибке - попробуйте перезапустить его через команду /start или выбрать эту же команду через меню 
\nЕсли и это не помогает - пишите @alexpure
'''


category_list = ['Инвестиции', 'Земельные участки', 'Дома', ]
menu_list = ['Контакты', 'Заказать звонок', 'Помощь', 'Видео обзоры']
back_list = ['↩ Назад', '× Отмена', '↩ Главное меню']
kush_list = ['до 1 млн', '1 - 3 млн', '3+ млн',
             '5 - 7 млн', '7 - 10 млн', '10+ млн']
teh_channel = -1001511156970
