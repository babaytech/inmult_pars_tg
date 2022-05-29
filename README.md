## Бот телеграмм для парсинга зарубежных мультфильмо
---
Установка и запуск ~~довльно сложен~~<br>
Потребуется установленный python3 и pip<br>
В консоли вводим
```no-highlight
pip install aiogram
pip install configparser
pip install wget
pip install colorama
pip install BeautifulSoup4
pip install requests
pip install lxml
```
После установки пакетов запускаем как обычное приложение<br>
Но требуется выбрать запуск через python3
## 1. Первичный запуск
---
Для первого запуска в файле config.ini
Требуется ввести свой токен который вы получили у botfather
```no-highliht
token = "you both token"
```
Вводить токен требуется без ковычек 
Так же надо будет выбрать систему на которой вы будите его запускать
```no-highliht
termux = False
linux = True
windows = False
```
Выбирать стоит одну систему
Иначе будет ошибка и бот не запуститься
