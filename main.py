#####################################################################
import config
import sqlite3
import parser.south_park, parser.serials_pars
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


bot = Bot(token = '')
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

    for row in cursor.execute(f"SELECT * FROM south_park WHERE sezon=1"):
        await message.answer(f'"{row[0]}"\n{row[2]}')
        # await bot.send_video(chat_id=message.from_user.id, video=row[2], caption=row[2])


@dp.message_handler(lambda message: message.text == "Рик и Морти")
async def without_puree(message: types.Message):
    await message.answer("в разработке\nХватит терпения то дождётесь :)")


@dp.message_handler(commands="update_db")
async def cmd_test1(message: types.Message):
    await message.answer("ожидайте")
    parser.south_park.main_mult()
    await message.answer("готово")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    conn.close()
    # parser.mult_pars.main_mult()



