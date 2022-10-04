import os
import time

import pandas as pd
import schedule
import sqlalchemy as sa
from dotenv import load_dotenv

from utils import gsheet2df, usd_rate

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", default='postgres')
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default='postgres')
DB_HOST = os.getenv("DB_HOST", default='db')
DB_NAME = os.getenv("DB_NAME", default='postgres')
DB_PORT = os.getenv("DB_PORT", default='5432')

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:" \
         f"{DB_PORT}/{DB_NAME}"


def send_to_db():
    """
    Отправляем данные из таблицы в БД.
    Если БД существует, то данные обновляются.
    :return:
    """
    orders = gsheet2df('test', 0)
    orders['стоимость в руб.'] = orders['стоимость,$'] * usd_rate()
    orders['срок поставки'] = pd.to_datetime(
        orders['срок поставки'],
        format='%d.%m.%Y'
    ).dt.date

    connection_string = DB_URL
    engine = sa.create_engine(connection_string)
    engine.connect()

    orders.to_sql(
        'orders',
        con=engine,
        dtype={
            '№': sa.BIGINT,
            'заказ №': sa.BIGINT,
            'стоимость,$': sa.BIGINT,
            'срок поставки': sa.VARCHAR,
            'стоимость в руб.': sa.FLOAT,
        },
        if_exists='replace',
    )


def main():
    send_to_db()


if __name__ == '__main__':
    main()
    # планировщик запускает скрипт каждую минуту для проверки изменений
    schedule.every(1).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
