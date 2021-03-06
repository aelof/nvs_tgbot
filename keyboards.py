from telebot import types

hide_markup = types.ReplyKeyboardRemove()

menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, input_field_placeholder=' ')
btn1 = types.KeyboardButton('Найти объект')
btn2 = types.KeyboardButton('Контакты')
btn3 = types.KeyboardButton('Заказать звонок')
btn4 = types.KeyboardButton('Видео обзоры')
btn5 = types.KeyboardButton('Помощь')
menu_markup.add(btn1, btn2, btn3, btn4, btn5)

general_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, input_field_placeholder=' ')
btn1 = types.KeyboardButton('Инвестиции')
btn2 = types.KeyboardButton('Земельные участки')
btn3 = types.KeyboardButton('Дома')
btn4 = types.KeyboardButton('↩ Назад')
general_markup.add(btn1, btn2, btn3, btn4)

geo_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn1 = types.KeyboardButton('Геленджик')
btn2 = types.KeyboardButton('Анапа')
btn3 = types.KeyboardButton('Лаго-Наки')
btn4 = types.KeyboardButton('× Отмена')
geo_markup.add(btn1, btn2, btn3, btn4)

kush_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn1 = types.KeyboardButton('до 1 млн')
btn2 = types.KeyboardButton('1 - 3 млн')
btn3 = types.KeyboardButton('3+ млн')
btn4 = types.KeyboardButton('↩ Назад')
kush_markup.add(btn1, btn2, btn3, btn4)


kush_house_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn1 = types.KeyboardButton('5 - 7 млн')
btn2 = types.KeyboardButton('7 - 10 млн')
btn3 = types.KeyboardButton('10+ млн')
btn4 = types.KeyboardButton('↩ Назад')
kush_house_markup.add(btn1, btn2, btn3, btn4)

phone_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
btn1 = types.KeyboardButton('Поделиться номером', request_contact=True)
btn2 = types.KeyboardButton('× Отмена')
phone_markup.add(btn1, btn2)

order_call_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
btn1 = types.KeyboardButton('Да, заказать')
btn2 = types.KeyboardButton('× Отмена')
order_call_kb.add(btn1, btn2)


# --- INLINE KEYBOARDS ---

yt_markup = types.InlineKeyboardMarkup(row_width=1)
btn1 = types.InlineKeyboardButton('Все видео', url='https://www.youtube.com/c/НовоСтройНедвижимость/videos')
btn2 = types.InlineKeyboardButton('Плейлисты', url='https://www.youtube.com/c/НовоСтройНедвижимость/playlists')
btn3 = types.InlineKeyboardButton('Канал', url='https://www.youtube.com/channel/UCRXMqWZwA6bH8DSd6SCOezg')
yt_markup.add(btn1, btn2, btn3)
