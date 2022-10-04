# Парсер Google таблицы

# Описание проекта
### Приложение, которое парсит Google Sheets, складывает инфу в базу данных и конвертирует цену в рублях по курсу ЦБ.
### Так же следит за текущими заказами и если один или несколько заказов просрочены - отправляет уведомления в телеграм.

### Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

## Запуск в docker контейнерах:
- Клонируем репозиторий: 
```bash
git@github.com:potapovjakov/kanalservice.git
```
- Устанавливаем докер:
```bash
sudo apt update && sudo apt upgrade -y
sudo wget -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo wget -SL https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-linux-x86_64 -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
```
- Копируем таблицу себе в аккаунт
- Создаем сервисный аккаунт в Google API (https://support.google.com/a/answer/7378726?hl=ru)
- Скачанный файл с ключами переименовываем в  ```credentials.json``` и копируем в папку ```infra```
- Так же в папке ```infra``` создаем файл ```.env``` и заполняем его актуальными значениями:
```
DB_NAME=название бд
POSTGRES_USER=имя пользователя бд
POSTGRES_PASSWORD=пароль пользователя бд
DB_HOST=хост бд
DB_PORT=порт бд
TG_TOKEN= Токен ТГ бота (получать у @BotFather)
CHAT_ID= ID аккаунта, на который бот будет пересылать сообщения(получать у @userinfobot)
```
- еще раз все проверяем и запускаем командой ```sudo docker-compose up --build``` из папки ```infra```

### Приложение создаст базу данных и заполнит ее значениями из таблицы. 
### Так же в базе данных будет столбец с ценой в рублях РФ.
### Если приложение не останавливать работать то:
- Планировщик будет проверять таблицу каждую минуту и если будут изменения то БД обновится.
- Если отправить телеграм боту сообщение /orders, то он немедленно пришлет все просроченные заказы
- Так же каждое утро в 9:00 МСК при наличии просроченных заказов будет приходить сообщение с общим количеством

#### Выполнил [Яков Потапов](https://github.com/potapovjakov)
