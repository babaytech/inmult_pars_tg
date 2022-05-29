#####################################################################
import configparser
import sqlite3
import parser.south_park, parser.rick_and_morty, parser.adventury_time, parser.love_death_and_robots
import colorama
import os
from moviepy.editor import *
import wget
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
#####################################################################

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(token=config["settings"]["token"])
dp = Dispatcher(bot)

conn = sqlite3.connect('serial.sqlite3')
cursor = conn.cursor()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Южный Парк", "Рик и Морти", "Любовь Смерть и Роботы", "Время Приключений"]
    keyboard.add(*buttons)
    await message.answer("Добро Пожаловать\nвыберите что хотите посмотреть", reply_markup=keyboard)

@dp.message_handler(commands="update_db")
async def cmd_test1(message: types.Message):
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
        number = 0
        db = "SELECT * FROM south_park"
        cursor.execute(db)
        url_db = cursor.fetchall()
        for row in url_db:
            download_urls = row[2]
            wget.download(download_urls, f"{number}.mp4")
            clip = VideoFileClip(f"{number}.mp4")
            resize = clip.resize(0.5)
            resize.write_videofile(f"{number}_resized.mp4")
            with open(f"{number}_resized.mp4", 'rb') as video:
                await message.answer_video(video)
            await message.answer(f"{number}.mp4 Загружен на сервер!")
            os.remove(f"{number}.mp4")
            os.remove(f"{number}_resized.mp4")
            number += 1


    if message.text == 'Рик и Морти':
        rm_btn_1 = InlineKeyboardButton(f'1 Сезон', callback_data='button1')
        rm_kb1 = InlineKeyboardMarkup().add(rm_btn_1)
        await message.reply('Выберете Сезон:', reply_markup=rm_kb1)

    if message.text == 'Любовь Смерть и Роботы':
        ldr_btn_1 = InlineKeyboardButton(f'1 Сезон', callback_data='button1')
        ldr_kb1 = InlineKeyboardMarkup().add(ldr_btn_1)
        await message.reply('Выберете Сезон:', reply_markup=ldr_kb1)

    if message.text == 'Время Приключений':
        ta_btn_1 = InlineKeyboardButton(f'1 Сезон', callback_data='button1')
        ta_kb1 = InlineKeyboardMarkup().add(ta_btn_1)
        await message.reply('Выберете Сезон:', reply_markup=ta_kb1)

def start_bot():
    executor.start_polling(dp, skip_updates=True)