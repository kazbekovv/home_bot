from aiogram import types
import logging
from config import dp, bot
from aiogram.utils import executor
from handlers import commands, echo

commands.register_commands(dp)


echo.register_echo(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)