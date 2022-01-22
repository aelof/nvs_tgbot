from telebot import types


menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, input_field_placeholder='Ориентируйтесь по кнопкам ниже')
btn1 = types.KeyboardButton('Найти объект')
btn2 = types.KeyboardButton('Контакты')
btn3 = types.KeyboardButton('Заказать звонок')
btn4 = types.KeyboardButton('Помощь')
menu_markup.add(btn1, btn2, btn3, btn4)

general_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, input_field_placeholder='Ориентируйтесь по кнопкам ниже')
btn1 = types.KeyboardButton('Инвестиции')
btn2 = types.KeyboardButton('Земельные участки')
btn3 = types.KeyboardButton('Дома')
btn4 = types.KeyboardButton('Видео обзоры')
general_markup.add(btn1, btn2, btn3, btn4)

geo_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn1 = types.KeyboardButton('Геленджик')
btn2 = types.KeyboardButton('Анапа')
btn3 = types.KeyboardButton('Лаго-Наки')
geo_markup.add(btn1, btn2, btn3)

kush_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn1 = types.KeyboardButton('до 1 млн')
btn2 = types.KeyboardButton('1 - 3 млн')
btn3 = types.KeyboardButton('3+ млн')
kush_markup.add(btn1, btn2, btn3)


kush_house_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn1 = types.KeyboardButton('5 - 7 млн')
btn2 = types.KeyboardButton('7 - 10 млн')
btn3 = types.KeyboardButton('10+ млн')
kush_house_markup.add(btn1, btn2, btn3)

