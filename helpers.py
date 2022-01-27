from enum import Enum
import sqlite3


conn = sqlite3.connect('Users.db', check_same_thread=False)
conn.row_factory = lambda cursor, row: row[0] # for output in list format instead tuple
cursor = conn.cursor()

def add_to_db(user_id, firstname, username, date):
    cursor.execute('INSERT INTO Users (user_id, firstname, username, date) VALUES (?, ?, ?, ?)', (user_id, firstname, username, date))
    conn.commit()


# try:
#     with con:
#         con.execute("insert into lang(name) values (?)", ("Python",))
# except sqlite3.IntegrityError:
#     print("couldn't add Python twice")

db_file = "database.vdb"    


class States(Enum):
    
    START = '0'
    ENTER_CAT = '1'
    ENTER_GEO = '2'
    ENTER_KUSH = '3'


class Target:
    QUERY = []

    def add_to_query(query):
        Target.QUERY.append(query)

    def show_query():
        return Target.QUERY

    def clear_query():
        Target.QUERY.clear()


hello = '''!
Я - специально обученный бот компании Новострой!
Могу помочь Вам <b>то-то и то-то</b>\n
Общаться мы будем с помощью клавиатуры с кнопками. Мне так понятнее понимать запрос.\n 
Сейчас Вы в <b>главном меню</b>, ориентируйтесь по кнопкам ниже  '''


def get_ids():
    cursor.execute('select user_id  from Users')
    return cursor.fetchall()
