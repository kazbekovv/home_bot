from aiogram import types, Dispatcher
from config import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']

async def game_dice(message: types.Message):
    bot_game = random.choice(games)
    player_game = random.choice(games)
    if games.index(bot_game) > games.index(player_game):
        result = 'bot win'
    elif games.index(bot_game) < games.index(player_game):
        result = 'you win'
    else:
        result = "Ничья!"

    await message.answer(f"{bot_game}")
    await message.answer(f"{player_game}")
    await message.answer(f"{result}")




def register_game(dp: Dispatcher):
    dp.register_message_handler(game_dice, commands=['game'])
