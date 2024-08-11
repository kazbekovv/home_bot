from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

size_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
size_buttons.add(KeyboardButton("XL"), KeyboardButton("3XL"), KeyboardButton("S"), KeyboardButton("M"), KeyboardButton("L"))

choose_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
choose_buttons.add(KeyboardButton("Да")).add(KeyboardButton("Нет"))