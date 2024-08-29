from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
import re
from aiogram.types import ReplyKeyboardRemove
from Google_sheets.sheets import get_google_sheets_data, update_google_sheet_registration

class FSM_reg(StatesGroup):
    fullname = State()
    age = State()
    email = State()
    gender = State()
    phone = State()
    photo = State()
    telegram_id = State()

async def fsm_start(message: types.Message):
    telegram_id = message.from_user.id
    data = get_google_sheets_data()

    for row in data:
        if row and row[0] == str(telegram_id):  # Предполагается, что telegram_id хранится в первой колонке
            await message.answer("Вы уже есть в нашей базе!")
            return

    await message.answer(text='Привет! \n'
                              'Напиши своё фио:\n\n'
                              '!Для того чтобы воспользоваться командами, '
                              'нажмите на "Отмена"!', reply_markup=buttons.cancel)
    await FSM_reg.fullname.set()

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text

    await FSM_reg.next()
    await message.answer(text='Укажите свой возраст:')

async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await FSM_reg.next()
    await message.answer(text='Укажите свою почту:')

async def load_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        email = message.text.strip()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            await message.answer("Некорректный формат электронной почты!")
            return
        data['email'] = email

    await FSM_reg.next()
    await message.answer(text='Укажите свой пол:')

async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

    await FSM_reg.next()
    await message.answer(text='Укажите свой номер телефона:')

async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await FSM_reg.next()
    await message.answer(text='Отправьте нам свою фотографию:')

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        data['telegram_id'] = message.from_user.id  # Сохраняем telegram_id в состояние

    try:
        update_google_sheet_registration(data)
    except Exception as e:
        print(f"Error in update_google_sheet_registration: {e}")

    kb = types.ReplyKeyboardRemove()

    await message.answer_photo(photo=data['photo'],
                               caption=f"Ваше фио - {data['fullname']}\n"
                                       f"Возраст - {data['age']}\n"
                                       f"Почта - {data['email']}\n"
                                       f"Пол - {data['gender']}\n"
                                       f"Номер тел - {data['phone']}\n"
                               )
    await message.answer(text='Спасибо за регистрацию!)', reply_markup=kb)
    await state.finish()

async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено!')

def register_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True),
                                state="*")

    dp.register_message_handler(fsm_start, commands=['registration'])
    dp.register_message_handler(load_name, state=FSM_reg.fullname)
    dp.register_message_handler(load_age, state=FSM_reg.age)
    dp.register_message_handler(load_email, state=FSM_reg.email)
    dp.register_message_handler(load_gender, state=FSM_reg.gender)
    dp.register_message_handler(load_phone, state=FSM_reg.phone)
    dp.register_message_handler(load_photo, state=FSM_reg.photo,
                                content_types=['photo'])
