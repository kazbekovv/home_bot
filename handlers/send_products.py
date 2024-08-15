import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import buttons


def get_db_connection():
    conn = sqlite3.connect('db/db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()

    products = conn.execute("""
        SELECT * FROM products p 
        INNER JOIN products_details pd ON p.id_product = pd.id_product  
    """).fetchall()

    conn.close()
    return products


def fetch_products_by_id(product_id):
    conn = get_db_connection()
    product = conn.execute("""
    SELECT p.id, p.name, p."size", p.price, p.id_product, p.photo, pd.category, pd.info_product  
    FROM products p 
    INNER JOIN products_details pd ON p.id_product = pd.id_product 
    WHERE p.id = ?
    """, (product_id,)).fetchone()
    conn.close()
    return product


async def start_sending_products(message: types.Message):
    products = fetch_all_products()
    if products:
        await send_product(message, products[0]['id'])
    else:
        await message.answer("Товары не найдены")


async def send_product(message: types.Message, product_id):
    product = fetch_products_by_id(product_id)

    if product:
        caption = (f"Название товара - {product['name']}\n"
        f"Информация о товаре - {product['info_product']}\n"
        f"Категория - {product['category']}\n"
        f"Размер - {product['size']}\n"
        f"Цена - {product['price']}\n"
        f"Артикул - {product['id_product']}")

        keyboard = InlineKeyboardMarkup()
        next_buttons = InlineKeyboardButton("Далее",
                                            callback_data=f'next_{product_id}')
        keyboard.add(next_buttons)

        await message.answer_photo(photo=product['photo'],
                                   caption=caption,
                                   reply_markup=keyboard)
    else:
        await message.answer("Товаров нет!")



async def next_product(callback_query: types.CallbackQuery):
    current_products_id = int(callback_query.data.split('_')[1])

    products = fetch_all_products()

    current_index = None

    for index, product in enumerate(products):
        if product['id'] == current_products_id:
            current_index = index
            break


    if current_index is not None and current_index < len(products) - 1:
        next_product_id = products[current_index + 1]['id']
        await send_product(callback_query.message, next_product_id)

    else:
        await callback_query.message.answer('No more products')

    await callback_query.answer()


def register_send_products_handler(dp: Dispatcher):
    dp.register_message_handler(start_sending_products, commands=['products'])
    dp.register_callback_query_handler(next_product, Text(startswith='next_'))