from google.oauth2 import service_account
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE = "lesson-44-2.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('sheets', 'v4', credentials=creds)
SHEET_ID = '1ltkKXYb-Woo5j-OEX9NjLijnZzSxf05JettZN_sipQo'

def update_fsm_sheet():
    fsm_data = [
        ["Состояние", "Событие", "Новое состояние", "Действие", "Условие"],
        ["fullname", "Получен запрос", "age", "Сохранение ФИО", "Не задано"],
        ["age", "Получен возраст", "email", "Сохранение возраста", "Возраст задан"],
        ["email", "Получен email", "gender", "Сохранение email", "Email валиден"],
        ["gender", "Получен пол", "phone", "Сохранение пола", "Пол задан"],
        ["phone", "Получен телефон", "photo", "Сохранение телефона", "Телефон задан"],
        ["photo", "Получена фотография", "Завершено", "Сохранение фотографии", "Фотография получена"]
    ]

    sheet = service.spreadsheets()
    request = sheet.values().update(
        spreadsheetId=SHEET_ID,
        range='Sheet1!A1:E7',
        valueInputOption='RAW',
        body={'values': fsm_data}
    )
    response = request.execute()
    print('Таблица обновлена:', response)