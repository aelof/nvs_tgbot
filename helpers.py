from enum import Enum
import string


hello = '''!
Я - специально обученный бот компании Новострой!
Могу помочь Вам <b>то-то и то-то</b>\n
Общаться мы будем с помощью клавиатуры с кнопками. Мне так понятнее понимать запрос.\n 
Сейчас Вы в <b>главном меню</b>, ориентируйтесь по кнопкам ниже  '''

category_list = ['Инвестиции', 'Земельные участки', 'Дома', 'Видео обзоры']


db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
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