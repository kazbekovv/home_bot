# CRON - (Command Run On) - Это система для автоматического запуска задач
                            # в определенное время

# Нужно установить библиотеку - apscheduler

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Импортирует AsyncIOScheduler из библиотеки apscheduler.
# Этот планировщик позволяет запускать задачи асинхронно в событиях asyncio.

import datetime
# Импортируем стандартный модуль datetime, который используется для работы с датой и временем

from config import bot

from apscheduler.triggers.cron import CronTrigger
# Импортирует CronTrigger, который используется для задания расписания запуска задач по CRON выражению.

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import random


users = [1014174749, ]
# Определяет список users, который содержит telegram id пользователя, для отправки уведомлений, В данном случае в список включен один пользователь

notification = []
# Создаем пустой список, в который будут добавляться сообщения для уведомлений




class Notification(StatesGroup):
    waiting_for_message = State()
# Состояние waiting_for_message будет использовано для ожидания текста уведомления от пользователя


async def send_notification():
    for user in users:
        if notification:
            message = random.choice(notification)
        else:
            message = 'У вас нет запланированных задач!'
        await bot.send_message(chat_id=user,
                               text=f"🔔 Напоминание 🔔 \n"
                                    f"Добрый день! "
                                    f"Не забудьте про - {message}")
# Асинхронная функция send_notification отправляет уведомления всем пользователям из списка users
# Если список notification не пуст, функция выберает случайное сообщение и отправляется его
# Если список пуст, отправляет сообщение по умолчанию.


async def set_scheduler():
    scheduler = AsyncIOScheduler(timezone='Asia/Bishkek')
    scheduler.add_job(send_notification,
                      CronTrigger(hour='21',
                                  minute='10',
                                  start_date=datetime.datetime.now()
                                  ),
                      )
    scheduler.start()
# Асинхронная функция set_scheduler создает и настраивает планировщик задач AsyncIOScheduler.
# В данном случае задача send_notification будет запускаться каждый день в 20:41 по времени зоны Asia/Bishkek.

# CronTrigger — это один из типов триггеров, предоставляемых библиотекой apscheduler, который используется для запуска задач по расписанию, основанному на CRON-выражениях.
# Этот триггер позволяет настроить время и частоту выполнения задач

# Основные параметры CronTrigger

	# •	year: Год, когда должна выполняться задача. Можно указать конкретный год или диапазон.
	# •	month: Месяц (1-12 или ‘jan’, ‘feb’, …).
	# •	day: День месяца (1-31).
	# •	week: Неделя года (1-53).
	# •	day_of_week: День недели (0-6 или ‘mon’, ‘tue’, …).
	# •	hour: Часы (0-23).
	# •	minute: Минуты (0-59).
	# •	second: Секунды (0-59).
	# •	start_date: Дата начала (можно указать точное время начала выполнения задач).
	# •	end_date: Дата окончания (после этой даты задачи больше не будут запускаться).
	# •	timezone: Временная зона, в которой выполняется задача.


async def handler_notification_command(message: types.Message):
    await message.reply('Введите сообщение для уведомления: ')
    await Notification.waiting_for_message.set()
# Асинхронная функция handler_notification_command обрабатывает команду /notification.
# При вызове этой команды бот просит пользователя ввести сообщение для уведомления и переводит его в состояние ожидания текста Notification.waiting_for_message.


async def handle_notification_text(message: types.Message, state: FSMContext):
    notification_message = message.text
    notification.append(notification_message)

    await message.reply(f'Сообщение "{notification_message}" добавлено в список уведомления')
    await state.finish()
# Асинхронная функция handle_notification_text обрабатывает введенный текст уведомления.
# Полученный текст добавляется в список notification, после чего пользователь получает подтверждение.
# Состояние заканчивается вызовом state.finish().


def register_notification(dp: Dispatcher):
    dp.register_message_handler(handler_notification_command, commands=['notification'])
    dp.register_message_handler(handle_notification_text, state=Notification.waiting_for_message)