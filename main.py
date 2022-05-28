#####################################################################
import configparser
import sqlite3
import parser.south_park, parser.rick_and_morty, parser.adventury_time, parser.love_death_and_robots
import colorama
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
#####################################################################


print(colorama.Fore.RED + " _____                         _               _            _     ")
print(colorama.Fore.RED + "/  ___|                       (_)             | |          | |    ")
print(colorama.Fore.RED + "\ `--.  __ _ _ __   __ _ _   _ _ _ __   ___   | |_ ___  ___| |__  ")
print(colorama.Fore.RED + " `--. \/ _` | '_ \ / _` | | | | | '_ \ / _ \  | __/ _ \/ __| '_ \ ")
print(colorama.Fore.RED + "/\__/ / (_| | | | | (_| | |_| | | | | |  __/  | ||  __/ (__| | | |")
print(colorama.Fore.RED + "\____/ \__,_|_| |_|\__, |\__,_|_|_| |_|\___|   \__\___|\___|_| |_|")
print(colorama.Fore.RED + "                    __/ |                                         ")
print(colorama.Fore.RED + "                   |___/                                          \n")
print(colorama.Fore.RESET)

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(token=config["settings"]["token"])
dp = Dispatcher(bot)

conn = sqlite3.connect('serial.sqlite3')
cursor = conn.cursor()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Южный Парк", "Рик и Морти"]
    keyboard.add(*buttons)
    await message.answer("Добро Пожаловать\nвыберите что хотите посмотреть", reply_markup=keyboard)


@dp.message_handler(Text(equals="Южный Парк"))
async def with_puree(message: types.Message):
    pass


@dp.message_handler(lambda message: message.text == "Рик и Морти")
async def without_puree(message: types.Message):
    pass


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


if __name__ == '__main__':
    print(config["DEFAULT"]["version"])
    executor.start_polling(dp, skip_updates=True)
    conn.close()
    # parser.mult_pars.main_mult()



