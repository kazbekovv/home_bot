from Google_sheets.config_sheets import service, google_sheet_id_users
from aiogram import Dispatcher, types
from config import dp


def update_google_sheet_products(name, size, price, id_product, category, info_product, collection):
    try:
        range_name = "Лист1!A:G"

        row = [name, size, price, id_product, category, info_product, collection]

        service.spreadsheets().values().append(
            spreadsheetId=google_sheet_id_users,
            range=range_name,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        print(row)

    except Exception as e:
        print(e)


def get_google_sheets_data():
    try:
        range_name = "Лист1!A:G"
        result = service.spreadsheets().values().get(
            spreadsheetId=google_sheet_id_users,
            range=range_name
        ).execute()
        rows = result.get('values', [])

        return rows

    except Exception as e:
        print(e)
        return []


async def send_data(message: types.Message):
    data = get_google_sheets_data()

    if not data:
        await message.reply("No data found.")

    else:
        headers = data[0]
        response = "Данные из Google Таблицы:\n\n"

        for row in data[1:]:
            for header, value in zip(headers, row):
                response += f"{header}: {value}\n"
            response += "\n"
        await message.reply(response)





def register_sheets(dispatcher: Dispatcher):
    dp.register_message_handler(send_data, commands=['get_sheets'])