#####################################################################
import configparser
from loguru import logger
import sqlite3
import parser.south_park, parser.rick_and_morty, parser.adventury_time, parser.love_death_and_robots
import wget
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
#####################################################################


config = configparser.ConfigParser()
config.read('config.ini')

storage = MemoryStorage()
bot = Bot(token=config["settings"]["token"])
dp = Dispatcher(bot, storage=storage)

conn_mult = sqlite3.connect('serial.sqlite3')
cursor_mult = conn_mult.cursor()

conn_tg = sqlite3.connect('telegram.sqlite3')
cursor_tg = conn_tg.cursor()

logger.add("logs/log.log", compression="zip", rotation="500 MB")

class UserState(StatesGroup):
    sezon = State()
    seriya = State()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    cursor_tg.execute("INSERT INTO users VALUES(?)", (username,))
    conn_tg.commit()
    logger.info(f"{username} подключился к боту")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Южный Парк", "Рик и Морти", "Любовь Смерть и Роботы", "Время Приключений"]
    keyboard.add(*buttons)
    await message.answer(f"Добро Пожаловать, {username}.\nвыберите что хотите посмотреть", reply_markup=keyboard)

@dp.message_handler(commands="update_db")
async def parse_mult_db(message):
    username = message.from_user.username if message.from_user.username else None
    logger.info(f"{username} обновляет базу данных")
    await message.answer("ожидайте")
    parser.love_death_and_robots.main_mult()
    await message.answer("Любовь Смерть и Роботы записан в базу данных")
    parser.adventury_time.main_mult()
    await message.answer("Время Приключений записан в базу данных")
    parser.rick_and_morty.main_mult()
    await message.answer("Рик и Морти записан в базу данных")
    parser.south_park.main_mult()
    await message.answer("Южный Парк записан в базу данных")

@dp.message_handler(commands="download_video")
async def download_video(message : types.Message):
    username = message.from_user.username if message.from_user.username else None
    logger.info(f"{username} нажал кнопку Скачивание файлов")
    db = "SELECT * FROM south_park"
    await message.answer("Ожидайте Отправки Видео")

    logger.debug("Запуск Скачивания Серий Южного Парка")
    cursor_mult.execute(db)
    url_db = cursor_mult.fetchall()
    for row in url_db:
        seriya = row[1]
        sezon = row[2]
        download_urls = row[3]
        wget.download(download_urls, f"mults/south_park/SP_{sezon}_{seriya}.mp4")
        await message.answer(f"Южный Парк сезон:{sezon} серия:{seriya} Загружен")
        logger.success(f"Южный Парк сезон:{sezon} серия:{seriya} Загружен")

    db = "SELECT * FROM rick_and_morty"
    logger.debug("Запуск Скачивания Серий Рик и Морти")
    cursor_mult.execute(db)
    url_db = cursor_mult.fetchall()
    for row in url_db:
        seriya = row[1]
        sezon = row[2]
        download_urls = row[3]
        wget.download(download_urls, f"mults/rick_and_morty/RK_{sezon}_{seriya}.mp4")
        await message.answer(f"Рик и Морти сезон:{sezon} серия:{seriya} Загружен")
        logger.success(f"Рик и Морти сезон:{sezon} серия:{seriya} Загружен")

    db = "SELECT * FROM love_death_and_robots"
    logger.debug("Запуск Скачивания Серий Любовь, Смерть и Роботы")
    cursor_mult.execute(db)
    url_db = cursor_mult.fetchall()
    for row in url_db:
        seriya = row[1]
        sezon = row[2]
        download_urls = row[3]
        wget.download(download_urls, f"mults/love_death_and_robots/LDR_{sezon}_{seriya}.mp4")
        await message.answer(f"Любовь, Смерть и Роботы сезон:{sezon} серия:{seriya} Загружен")
        logger.success(f"Любовь, Смерть и Роботы сезон:{sezon} серия:{seriya} Загружен")

    db = "SELECT * FROM adventure_time"
    logger.debug("Запуск Скачивания Серий Времени Приключений")
    cursor_mult.execute(db)
    url_db = cursor_mult.fetchall()
    for row in url_db:
        seriya = row[1]
        sezon = row[2]
        download_urls = row[3]
        wget.download(download_urls, f"mults/adventure_time/AT_{sezon}_{seriya}.mp4")
        await message.answer(f"Время приключений сезон:{sezon} серия:{seriya} Загружен на сервер!")
        logger.success(f"Время приключений сезон:{sezon} серия:{seriya} Загружен!")

@dp.message_handler(content_types=["video"])
async def video_file_id(message: types.Message):
    if config["settings"]["get_id_video"] == "True":
        video_id = message.video.file_id
        video_name = message.video.file_name
        logger.debug(f"id видео:{video_id} название видео:{video_name}")
        rm_name = video_name.find("RM")
        sp_name = video_name.find("SP")
        at_name = video_name.find("AT")
        ldr_name = video_name.find("LDR")
        if (rm_name >= 0):
            cursor_tg.execute("INSERT INTO rick_and_morty VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")

        if (sp_name >= 0):
            cursor_tg.execute("INSERT INTO south_park VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")

        if (at_name >= 0):
            cursor_tg.execute("INSERT INTO adventure_time VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")

        if (ldr_name >= 0):
            cursor_tg.execute("INSERT INTO love_death_and_robots VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")


    if config["settings"]["get_id_video"] == "False":
        logger.debug("переведите строку get_id_video в True если требуется")

@dp.message_handler(commands="write_id_video")
async def write_db_video(message: types.Message):
        await message.answer("Выберите номер сезона\n1-5 Сезон доступны")
        await UserState.sezon.set()

@dp.message_handler(state=UserState.sezon)
async def get_sezon(message: types.Message, state: FSMContext):
    await state.update_data(sezon=message.text)
    await message.answer("Теперь выберете серию\n1-11 серии")
    await UserState.next()

@dp.message_handler(state=UserState.seriya)
async def get_seriya(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else None
    await state.update_data(seriya=message.text)
    data = await state.get_data()
    try:
        cursor_tg.execute(f"SELECT * FROM rick_and_morty WHERE name_file = 'RM_{data['sezon']}_{data['seriya']}.mp4';")
        video_id_list = cursor_tg.fetchone()
        video_id = video_id_list[1]
        await bot.send_video(message.from_user.id, video=video_id)
        logger.debug(f"{username} выбрал Сезон:{data['sezon']} Серию:{data['seriya']}")
        await state.finish()
    except:
        logger.warning(f"{username} данных нет в базе!")
        await message.answer("такого номера нет в базе, введите другой номер!")



@dp.message_handler(content_types=["video"])
async def video_file_id(message: types.Message):
    if config["settings"]["get_id_video"] == "True":
        video_id = message.video.file_id
        video_name = message.video.file_name
        logger.debug(f"id видео:{video_id} название видео:{video_name}")
        rm_name = video_name.find("RM")
        sp_name = video_name.find("SP")
        at_name = video_name.find("AT")
        ldr_name = video_name.find("LDR")
        if (rm_name >= 0):
            cursor_tg.execute("INSERT INTO rick_and_morty VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")

        if (sp_name >= 0):
            cursor_tg.execute("INSERT INTO south_park VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")

        if (at_name >= 0):
            cursor_tg.execute("INSERT INTO adventure_time VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")

        if (ldr_name >= 0):
            cursor_tg.execute("INSERT INTO love_death_and_robots VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")


    if config["settings"]["get_id_video"] == "False":
        logger.debug("переведите строку get_id_video в True если требуется")


def start_bot():
    executor.start_polling(dp, skip_updates=True)