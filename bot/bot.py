#####################################################################
import configparser
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

logger.add("log.log", compression="zip", rotation="500 MB")

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Южный Парк", "Рик и Морти", "Любовь Смерть и Роботы", "Время Приключений"]
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
    if message.text == 'Южный Парк':
        username = message.from_user.username if message.from_user.username else None
        logger.debug(f"{username} нажал кнопку Южный Парк")
        number = 0
        db = "SELECT * FROM south_park"
        await message.answer("Ожидайте Отправки Видео")
        logger.info("Запуск Скачивания Серий Южного Парка")
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            download_urls = row[2]
            wget.download(download_urls, f"{number}.mp4")
            logger.info(f"Сжатие файла {number}.mp4")
            clip = VideoFileClip(f"{number}.mp4")
            resize = clip.resize(0.5)
            resize.write_videofile(f"{number}_resized.mp4")
            await message.answer_video(open(f'{number}_resized.mp4', 'rb'))
            await message.answer(f"{number}.mp4 Загружен на сервер!")
            os.remove(f"{number}.mp4")
            os.remove(f"{number}_resized.mp4")
            logger.info(f"файл {number}_resized.mp4 отправлен пользователю")
            number += 1

    if message.text == 'Рик и Морти':
        username = message.from_user.username if message.from_user.username else None
        logger.debug(f"{username} нажал кнопку Рик и Морти")
        number = 0
        db = "SELECT * FROM rick_and_morty"
        await message.answer("Ожидайте Отправки Видео")
        logger.info("Запуск Скачивания Серий Рик и Морти")
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            download_urls = row[2]
            wget.download(download_urls, f"{number}.mp4")
            logger.info(f"Сжатие файла {number}.mp4")
            clip = VideoFileClip(f"{number}.mp4")
            resize = clip.resize(0.5)
            resize.write_videofile(f"{number}_resized.mp4")
            await message.answer_video(open(f'{number}_resized.mp4', 'rb'))
            await message.answer(f"{number}.mp4 Загружен на сервер!")
            os.remove(f"{number}.mp4")
            os.remove(f"{number}_resized.mp4")
            logger.info(f"файл {number}_resized.mp4 отправлен пользователю")
            number += 1

    if message.text == 'Любовь Смерть и Роботы':
        username = message.from_user.username if message.from_user.username else None
        logger.debug(f"{username} нажал кнопку Любовь, Смерть и Роботы")
        number = 0
        db = "SELECT * FROM love_death_and_robots"
        await message.answer("Ожидайте Отправки Видео")
        logger.info("Запуск Скачивания Серий Любовь, Смерть и Роботы")
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            download_urls = row[2]
            wget.download(download_urls, f"{number}.mp4")
            logger.info(f"Сжатие файла {number}.mp4")
            clip = VideoFileClip(f"{number}.mp4")
            resize = clip.resize(0.5)
            resize.write_videofile(f"{number}_resized.mp4")
            await message.answer_video(open(f'{number}_resized.mp4', 'rb'))
            await message.answer(f"{number}.mp4 Загружен на сервер!")
            os.remove(f"{number}.mp4")
            os.remove(f"{number}_resized.mp4")
            logger.info(f"файл {number}_resized.mp4 отправлен пользователю")
            number += 1


    if message.text == 'Время Приключений':
        username = message.from_user.username if message.from_user.username else None
        logger.debug(f"{username} нажал кнопку Время Приключений")
        number = 0
        db = "SELECT * FROM adventure_time"
        await message.answer("Ожидайте Отправки Видео")
        logger.info("Запуск Скачивания Серий Времени Приключений")
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            download_urls = row[2]
            wget.download(download_urls, f"{number}.mp4")
            logger.info(f"Сжатие файла {number}.mp4")
            clip = VideoFileClip(f"{number}.mp4")
            resize = clip.resize(0.5)
            resize.write_videofile(f"{number}_resized.mp4")
            await message.answer_video(open(f'{number}_resized.mp4', 'rb'))
            await message.answer(f"{number}.mp4 Загружен на сервер!")
            os.remove(f"{number}.mp4")
            os.remove(f"{number}_resized.mp4")
            logger.info(f"файл {number}_resized.mp4 отправлен пользователю")
            number += 1

def start_bot():
    executor.start_polling(dp, skip_updates=True)