from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import dp

async def webapp_reply_button(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    geeks_online = KeyboardButton("Geeks Online",
                                  web_app=types.WebAppInfo(url="https://online.geeks.kg"))
    kaktus_media = KeyboardButton("Кактус Медиа",
                                  web_app=types.WebAppInfo(url="https://kaktus.media"))
    Netflix = KeyboardButton("Netflix",
                                  web_app=types.WebAppInfo(url="https://www.netflix.com/kg-ru/"))
    JutSu = KeyboardButton("JutSu",
                                  web_app=types.WebAppInfo(url="https://jut.su/"))
    ChatGpt = KeyboardButton("Netflix",
                                  web_app=types.WebAppInfo(url="https://chatgpt.com/"))


    keyboard.add(geeks_online, kaktus_media, Netflix, JutSu, ChatGpt)

    await message.answer(text='Нажми на кнопки для открытия сайтов', reply_markup=keyboard)


async def webapp_inline_button(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)

    geeks_online = InlineKeyboardButton("Geeks",
                                        web_app=types.WebAppInfo(url="https://online.geeks.kg"))
    kaktus_media = InlineKeyboardButton("Кактус Медиа",
                                        web_app=types.WebAppInfo(url="https://kaktus.media"))
    Netflix = InlineKeyboardButton("Netflix",
                                        web_app=types.WebAppInfo(url="https://www.netflix.com/kg-ru/"))

    JutSu = InlineKeyboardButton("Jut.Su",
                                   web_app=types.WebAppInfo(url="https://jut.su/"))

    ChatGpt = InlineKeyboardButton('ChatGpt', url="https://chatgpt.com/")

    keyboard.add(geeks_online, kaktus_media, Netflix, JutSu, ChatGpt)

    await message.answer(text='Нажми на кнопки для открытия сайтов', reply_markup=keyboard)


def register_webapp_handlers(dispatcher: Dispatcher):
    dp.register_message_handler(webapp_reply_button, commands=['webreply'])
    dp.register_message_handler(webapp_inline_button, commands=['webinline'])