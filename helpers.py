from enum import Enum
import sqlite3

# db file to class States 
db_file = "database.vdb"    


conn = sqlite3.connect('Users.db', check_same_thread=False)
conn.row_factory = lambda cursor, row: row[0] # for output in list format instead tuple
cursor = conn.cursor()

def add_to_db(user_id, firstname, username, date):
    cursor.execute('INSERT INTO Users (user_id, firstname, username, date) VALUES (?, ?, ?, ?)', (user_id, firstname, username, date))
    conn.commit()


def get_ids():
    cursor.execute('select user_id  from Users')
    return cursor.fetchall()

def db_get_link(where, what, how):
    conn = sqlite3.connect('links.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT Ссылка FROM Sheet1 WHERE Территория=? AND Категория=?  AND Бюджет=?', (where, what, how) )
        return cursor.fetchone()
    except:
        return False

def db_insert_phone(user_id, phone):
    cursor.execute(f'UPDATE Users SET phone = ? WHERE user_id = ? ', (phone, user_id))
    conn.commit()


def exist_phone(user_id):
    cursor.execute('SELECT phone FROM Users WHERE user_id=user_id' )
    if cursor.fetchone():
        return True
    else:
        return False




class States(Enum):
    
    START = '0'
    GEO = '1'
    CAT = '2'
    KUSH = '3'
    PHONE = '4'


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
Могу помочь Вам <b>то-то и то-то</b>\n
Общаться мы будем с помощью клавиатуры с кнопками. Мне так понятнее понимать запрос.\n 
Сейчас Вы в <b>главном меню</b>, ориентируйтесь по кнопкам ниже \n
<i>Если вы не знакомы с ботом - советуем обратиться за помощью, выбрав "Помощь" на клавиатуре ниже </i>'''

help = ''' В основном вся коммуникация с ботом будет происходить через встроенную клавиатуру\n
Почти всё общение сводиться к ответу на вопросы путём выбора вариантов ответа на клавиатуре снизу\n 
Если вдруг бот перестал отвечать или сообщает об ошибке - попробуйте перезапустить его через команду /start или выбрать эту же команду через меню 
\nЕсли и это не помогает - пишите @alexpure - он поможет
'''

