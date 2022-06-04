#####################################################################
import configparser
import os

from loguru import logger
import sqlite3
import parser.south_park, parser.rick_and_morty, parser.adventury_time, parser.love_death_and_robots
from moviepy.editor import *
import wget
from aiogram import Bot, Dispatcher, executor, types
#####################################################################

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(token=config["settings"]["token"])
dp = Dispatcher(bot)

conn = sqlite3.connect('serial.sqlite3')
cursor = conn.cursor()

logger.add("logs/log.log", compression="zip", rotation="500 MB")

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Южный Парк", "Рик и Морти", "Любовь Смерть и Роботы", "Время Приключений", "Скачивание файлов"]
    keyboard.add(*buttons)
    username = message.from_user.username if message.from_user.username else None
    logger.debug(f"{username} подключился к боту")
    await message.answer("Добро Пожаловать\nвыберите что хотите посмотреть", reply_markup=keyboard)


@dp.message_handler(commands="update_db")
async def cmd_test1(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    logger.debug(f"{username} обновляет базу данных")
    await message.answer("ожидайте")
    parser.love_death_and_robots.main_mult()
    await message.answer("Любовь Смерть и Роботы записан в базу данных")
    parser.adventury_time.main_mult()
    await message.answer("Время Приключений записан в базу данных")
    parser.rick_and_morty.main_mult()
    await message.answer("Рик и Морти записан в базу данных")
    parser.south_park.main_mult()
    await message.answer("Южный Парк записан в базу данных")
    await message.answer("Готово")

@dp.message_handler(content_types=['text'])
async def main_btn(message : types.Message):
    if message.text == 'Скачивание файлов':
        username = message.from_user.username if message.from_user.username else None
        logger.debug(f"{username} нажал кнопку Скачивание файлов")
        db = "SELECT * FROM south_park"
        await message.answer("Ожидайте Отправки Видео")
        logger.info("Запуск Скачивания Серий Южного Парка")
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            seriya = row[1]
            sezon = row[2]
            download_urls = row[3]
            wget.download(download_urls, f"mults/south_park/{sezon}_{seriya}.mp4")
            # logger.info(f"Сжатие файла {number}.mp4")
            await message.answer(f"Южный Парк сезон:{sezon} серия:{seriya} Загружен")
            logger.info(f"Южный Парк сезон:{sezon} серия:{seriya} Загружен")

        db = "SELECT * FROM rick_and_morty"
        logger.info("Запуск Скачивания Серий Рик и Морти")
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            seriya = row[1]
            sezon = row[2]
            download_urls = row[3]
            wget.download(download_urls, f"mults/rick_and_morty/{sezon}_{seriya}.mp4")
            # logger.info(f"Сжатие файла {number}.mp4")
            await message.answer(f"Рик и Морти сезон:{sezon} серия:{seriya} Загружен")
            logger.info(f"Рик и Морти сезон:{sezon} серия:{seriya} Загружен")

        db = "SELECT * FROM love_death_and_robots"
        logger.info("Запуск Скачивания Серий Любовь, Смерть и Роботы")
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            seriya = row[1]
            sezon = row[2]
            download_urls = row[3]
            wget.download(download_urls, f"mults/love_death_and_robots/{sezon}_{seriya}.mp4")
            # logger.info(f"Сжатие файла {number}.mp4")
            await message.answer(f"Любовь, Смерть и Роботы сезон:{sezon} серия:{seriya} Загружен")
            logger.info(f"Любовь, Смерть и Роботы сезон:{sezon} серия:{seriya} Загружен")

        db = "SELECT * FROM adventure_time"
        logger.info("Запуск Скачивания Серий Времени Приключений")
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            seriya = row[1]
            sezon = row[2]
            download_urls = row[3]
            wget.download(download_urls, f"mults/adventure_time/{sezon}_{seriya}.mp4")
            # logger.info(f"Сжатие файла {number}.mp4")
            await message.answer(f"Время приключений сезон:{sezon} серия:{seriya} Загружен на сервер!")
            logger.info(f"Время приключений сезон:{sezon} серия:{seriya} Загружен!")

def start_bot():
    executor.start_polling(dp, skip_updates=True)