from datetime import datetime

import gspread
import pandas as pd
from cbrf.models import DailyCurrenciesRates
from oauth2client.service_account import ServiceAccountCredentials as sac


def gsheet2df(spreadsheet_name: str, sheet_num: int):
    """
    Получаем датафрейм из таблицы
    :param spreadsheet_name: имя таблицы
    :param sheet_num: номер листа, первый - нулевой
    :return: датафрейм
    """
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]

    credentials_path = 'credentials.json'
    credentials = sac.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)
    sheet = client.open(spreadsheet_name).get_worksheet(
        sheet_num).get_all_records()
    df = pd.DataFrame.from_dict(sheet)
    return df


def usd_rate():
    """Функция для получения последнего курса
    доллара ЦБ РФ на текущую дату.
    Валюта - Доллар США
    Дата - текущая
    """
    data = datetime.now()
    code = 'R01235'
    rate = DailyCurrenciesRates(data).get_by_id(code).value
    return rate
