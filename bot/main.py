import os
import time

import psycopg2
import telebot
from dotenv import load_dotenv

load_dotenv()


POSTGRES_USER = os.getenv("POSTGRES_USER", default='postgres')
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default='postgres')
DB_HOST = os.getenv("DB_HOST", default='db')
DB_NAME = os.getenv("DB_NAME", default='postgres')
DB_PORT = os.getenv("DB_PORT", default='5432')

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:" \
         f"{DB_PORT}/{DB_NAME}"
TG_TOKEN = os.getenv('TG_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TG_TOKEN)


def get_expired_orders():
    """
    Получает из БД заказы, срок поставки которых
    истек на текущую дату.
    :return:
    """
    connection = psycopg2.connect(DB_URL)
    cursor = connection.cursor()
    request = (
        f'SELECT "срок поставки", "заказ №" FROM orders  '
        f'WHERE "срок поставки"::date < CURRENT_DATE::date;'
    )
    cursor.execute(request)
    expired_orders = cursor.fetchall()
    return expired_orders


def count_expired_orders():
    """
    Выводит общее количество просроченных заказов и
    номер с датой каждого.
    :param data:
    :return:
    """
    data = get_expired_orders()
    if len(data) > 0:
        message_all = (
            f'Всего {len(data)} просроченных заказов.'
        )
        bot.send_message(
            CHAT_ID,
            message_all,
        )
        for i in data:
            message_cnt = f'Заказ номер {i[1]} c датой {i[0]} просрочен!'
            bot.send_message(
                CHAT_ID,
                message_cnt,
            )
            time.sleep(0.5)
    else:
        bot.send_message(
            CHAT_ID,
            'Просроченных заказов нет',
        )


def schedule_job_send(data):
    """
    Если приложение запущено, то бот будет каждый день присылать
    количество просроченных заказов(если они есть).
    :param data:
    :return:
    """
    data = get_expired_orders()
    if len(data) > 0:
        message_per_day = (
            f'Всего {len(data)} просроченных заказов.'
            f'Для просмотра детальной информации введите /orders'
        )
        bot.send_message(
            CHAT_ID,
            message_per_day,
        )


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    Бот по команде '/orders' отправляет все просроченные
     заказы с номером и датой.
    :param message:
    :return:
    """
    if message.text == "/orders":
        count_expired_orders()
    else:
        bot.send_message(
            message.from_user.id,
            "Я принимаю только /orders"
        )


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
