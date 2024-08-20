from aiogram import types, Dispatcher
from config import admin, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging


user_warnings = {}


async def welcome_user(message: types.Message):
    for member in message.new_chat_members:
        await message.answer(f"Добро пожаловать, {member.full_name}\n\n"
                             f"Правила группы:\n"
                             f"* Не спамить\n"
                             f"* Не материться\n"
                             f"* Обсуждение политических тем\n")


words = ['дурак', 'дебил', 'кретин', 'даун', 'амеба', 'израиль', 'украина', 'россия']


async def filter_word(message: types.Message):
    message_text = message.text.lower()
    for word in words:
        if word in message_text:
            user_id = message.from_user.id

            user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

            warnings_left = 3 - user_warnings[user_id]
            if warnings_left > 0:
                await message.answer(f"Не ругайся! У вас осталось {warnings_left} предупреждений.")
            else:
                await message.answer("Вы нарушили правила трижды. Вы будете удалены из чата.")
                await bot.kick_chat_member(message.chat.id, user_id)
                await bot.unban_chat_member(message.chat.id, user_id)
                user_warnings[user_id] = 0
            await message.delete()
            break


async def delete_user_handler(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in admin:
            await message.answer('Чорт, ты не админ!')
        elif not message.reply_to_message:
            await message.answer('Команда должна быть ответом на сообщение')
        else:
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.full_name

            if message.from_user.id in admin:
                await message.answer(f'Вы действительно хотите удалить {user_name} ?',
                                     reply_markup=InlineKeyboardMarkup().add(
                                         InlineKeyboardButton(f'Удалить',
                                                              callback_data=f'delete_user {user_id}')))
            else:
                await message.answer('Вы не имеете права удалять пользователей.')

    else:
        await message.answer('Эта команда должна быть использована в группе')


async def complete_delete_user(call: types.CallbackQuery):
    user_id = int(call.data.replace("delete_user ", ""))

    try:
        await bot.kick_chat_member(call.message.chat.id, user_id)
        await bot.unban_chat_member(call.message.chat.id, user_id)

        await call.answer(text='Пользователь удален!', show_alert=True)

        await bot.delete_messages(call.message.chat.id, call.message_id)
    except Exception as e:
        logging.error(f'Error in complete_delete_user: {e}')
        await call.answer(text='Не удалось удалить пользователя', show_alert=True)



async def pin_message(message: types.Message):
    if message.chat.type == 'group':
        if message.reply_to_message:
            await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
            await message.answer("Сообщение закреплено!")
        else:
            await message.answer("Команда !pin должна быть ответом на сообщение.")
    else:
        await message.answer("Эта команда может использоваться только в группах.")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(welcome_user,
                                content_types=[types.ContentType.NEW_CHAT_MEMBERS])
    dp.register_message_handler(delete_user_handler, commands=['delete'])
    dp.register_callback_query_handler(complete_delete_user,
                                       lambda call: call.data and call.data.startswith('delete_user '))
    dp.register_message_handler(filter_word)
    dp.register_message_handler(pin_message, commands=['pin'])
