from Google_sheets.config_sheets import service, google_sheet_id_users
from aiogram import Dispatcher, types
from config import dp


def update_google_sheet_registration(data):
    try:
        range_name = "Лист1!A:G"
        row = [
            data['telegram_id'],  # Добавляем telegram_id в первую колонку
            data['fullname'],
            data['age'],
            data['email'],
            data['gender'],
            data['phone'],
            data['photo']
        ]

        service.spreadsheets().values().append(
            spreadsheetId=google_sheet_id_users,
            range=range_name,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()

    except Exception as e:
        print(e)

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        data['telegram_id'] = message.from_user.id  # Сохраняем telegram_id в состояние

    # Запись данных в Google Sheets
    update_google_sheet_registration(data)

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