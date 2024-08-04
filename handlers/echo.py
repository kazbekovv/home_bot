from aiogram import types, Dispatcher

async def echo_handler(message: types.Message):
    text = message.text
    if text.isdigit():
        number = int(text)
        squared_number = number ** 2
        await message.answer(f'{squared_number}')
    else:
        await message.answer(text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo_handler)