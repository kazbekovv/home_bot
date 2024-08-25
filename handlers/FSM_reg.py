from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons

class StoreFSM(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_size = State()
    waiting_for_category = State()
    waiting_for_price = State()
    waiting_for_photo = State()
    confirming = State()  # Добавлено состояние confirming

async def start(message: types.Message):
    await message.answer("Введите название товара:")
    await StoreFSM.waiting_for_product_name.set()

async def process_product_name(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await message.answer("Выберите размер:", reply_markup=buttons.size_buttons)
    await StoreFSM.waiting_for_size.set()

async def process_size(message: types.Message, state: FSMContext):
    size = message.text
    await state.update_data(size=size)
    await message.answer("Введите категорию:")
    await StoreFSM.waiting_for_category.set()

async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Введите стоимость:")
    await StoreFSM.waiting_for_price.set()

async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Отправьте фотографию товара:")
    await StoreFSM.waiting_for_photo.set()

async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    product_name = data.get('product_name')
    size = data.get('size')
    category = data.get('category')
    price = data.get('price')
    telegram_id = message.from_user.id  # Получаем telegram_id пользователя

    await message.answer_photo(photo_id)
    await message.answer(f"Товар: {product_name}\nРазмер: {size}\nКатегория: {category}\nСтоимость: {price}")
    await message.answer("Верные ли данные?", reply_markup=buttons.choose_buttons)

    await sql_insert_sheet_data(telegram_id, product_name, size, category, price)

    await StoreFSM.confirming.set()

async def confirm_data(message: types.Message, state: FSMContext):
    if message.text == "Да":
        await message.answer("Сохранено в базу")
        # Вы можете добавить функцию сохранения в базу данных
    else:
        await message.answer("Вы можете начать заново, отправив команду /start")

    await state.finish()




def register_fsm(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(process_product_name, state=StoreFSM.waiting_for_product_name)
    dp.register_message_handler(process_size, state=StoreFSM.waiting_for_size)
    dp.register_message_handler(process_category, state=StoreFSM.waiting_for_category)
    dp.register_message_handler(process_price, state=StoreFSM.waiting_for_price)
    dp.register_message_handler(process_photo, state=StoreFSM.waiting_for_photo, content_types=['photo'])
    dp.register_message_handler(confirm_data, state=StoreFSM.confirming)

