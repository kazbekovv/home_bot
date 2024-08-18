from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons

class Form(StatesGroup):
    start = State()
    in_progress = State()
    collection = State()
    end = State()

# Хэндлер для начала работы с ботом
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await Form.start.set()
    await message.answer("Hello! Use /progress to move to the next stage.")

# Хэндлер для перехода в состояние 'collection'
@dp.message_handler(commands=['progress'], state=Form.start)
async def progress_command(message: types.Message, state: FSMContext):
    await Form.collection.set()
    await message.answer("You are now in the 'collection' stage.")

# Хэндлер для записи в таблицу
@dp.message_handler(commands=['add_product'], state=Form.collection)
async def add_product(message: types.Message, state: FSMContext):
    productid = 123  # Замените на динамическое получение ID продукта
    collection_name = "Sample Collection"  # Замените на динамическое получение названия коллекции

    # Добавление записи в базу данных
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO collection_products (productid, collection)
    VALUES (?, ?)
    ''', (productid, collection_name))
    conn.commit()
    conn.close()

    await message.answer(f"Product {productid} added to collection '{collection_name}'.")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
