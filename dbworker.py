
from vedis import Vedis
from helpers import States, db_file


# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
    with Vedis(db_file) as db:
        try:
            # Если используете Vedis версии ниже, чем 0.7.1, то .decode() НЕ НУЖЕН
            return db[user_id].decode()
        except KeyError:  # Если такого ключа почему-то не оказалось
            return States.START.value  # значение по умолчанию - начало диалога


# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    with Vedis(db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False
