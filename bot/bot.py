#####################################################################
import configparser
import requests
from loguru import logger
import sqlite3
import parser.south_park, parser.rick_and_morty, parser.adventury_time, parser.love_death_and_robots, parser.we_bare_bears
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


"""Запись нового пользователя в БД"""
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    try:
        cursor_tg.execute("INSERT INTO users VALUES(?)", (username,))
        conn_tg.commit()
        logger.info(f"{username} подключился к боту")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Просмотр мультфильмов", "Поддержка", "О нас"]
        keyboard.add(*buttons)
        await message.answer(f"Добро Пожаловать,{username}.\nвыберите что хотите посмотреть", reply_markup=keyboard)
    except:
        logger.info(f"{username} снова подключился к боту")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Просмотр мультфильмов", "Поддержка", "О нас"]
        keyboard.add(*buttons)
        await message.answer(f"Добро Пожаловать,{username}.\nвыберите что хотите посмотреть", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Просмотр мультфильмов")
async def with_puree(message: types.Message):
    await message.reply("Время Приключений - /adventure_time\n"
                        "Южный Парк - /south_park\n"
                        "Любовь Смерть и Роботы - /love_death_and_robots\n"
                        "Рик и Морти - /rick_and_morty\n"
                        "Мы Обычные Медведи - /we_bare_bears\n")

"""Парсинг ссылок для мультфильмов"""
@dp.message_handler(commands="update_db")
async def parse_mult_db(message):
    username = message.from_user.username if message.from_user.username else None
    cursor_tg.execute(f"SELECT * FROM users WHERE username = '{username}';")
    admin = cursor_tg.fetchone()
    if admin[1] == 1:
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
        parser.we_bare_bears.main_mult()
        await message.answer("Мы Обычные Медведи записан в базу данных")
    elif admin[1] == 0:
        logger.warning(f"{username} попытался обновить базу данных")
        await message.answer("куда лезешь заюш ?")


"""Скачивание мультфильмов из базы serial"""
@dp.message_handler(commands="download_video")
async def download_video(message : types.Message):
    username = message.from_user.username if message.from_user.username else None
    cursor_tg.execute(f"SELECT * FROM users WHERE username = '{username}';")
    admin = cursor_tg.fetchone()
    lvl_admin = admin[1]
    if lvl_admin == 1:
        logger.info(f"{username} нажал кнопку Скачивание файлов admin = {lvl_admin}")
        
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
            r = requests.get(download_urls)
            with open(f'mults/love_death_and_robots/WBB_{sezon}_{seriya}.mp4', 'wb') as f:
                f.write(r.content)

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
            r = requests.get(download_urls)
            with open(f'mults/adventure_time/_{sezon}_{seriya}.mp4', 'wb') as f:
                f.write(r.content)

            await message.answer(f"Время приключений сезон:{sezon} серия:{seriya} Загружен на сервер!")
            logger.success(f"Время приключений сезон:{sezon} серия:{seriya} Загружен!")

        db = "SELECT * FROM we_bare_bears"
        logger.debug("Запуск Скачивания Серий Мы Обычные Медведи")
        cursor_mult.execute(db)
        url_db = cursor_mult.fetchall()
        for row in url_db:
            seriya = row[1]
            sezon = row[2]
            download_urls = row[3]
            r = requests.get(download_urls)
            with open(f'mults/we_bare_bears/WBB_{sezon}_{seriya}.mp4', 'wb') as f:
                f.write(r.content)

            await message.answer(f"Мы Обычные Медведи сезон:{sezon} серия:{seriya} Загружен на сервер!")
            logger.success(f"Мы Обычные Медведи сезон:{sezon} серия:{seriya} Загружен!")

    elif admin == 0:
        logger.warning(f"{username} попытался скачать мультфильмы")
        await message.answer("куда лезешь заюш ?")


"""Получение id каждого полученного файла"""
@dp.message_handler(content_types=["video"])
async def video_file_id(message: types.Message):
    if config["settings"]["get_id_video"] == "True":
        video_id = message.video.file_id
        video_name = message.video.file_name
        logger.debug(f"id видео:{video_id} название видео:{video_name}")
        wbb_name = video_name.find("WBB")
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

        if (wbb_name >= 0):
            cursor_tg.execute("INSERT INTO we_bare_bears VALUES(?, ?)", (video_name, video_id))
            conn_tg.commit()
            logger.success(f"{video_name} сохранен в базу данных")


    if config["settings"]["get_id_video"] == "False":
        logger.debug("переведите строку get_id_video в True если требуется")


class UserState_RM(StatesGroup):
    sezon = State()
    seriya = State()
"""Запрос на получение номера сезона"""
@dp.message_handler(commands="rick_and_morty")
async def write_db_video_rick(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    logger.debug(f"{username} выбрал Рик и Морти")
    await message.answer("Выберите номер сезона\n1-5 Сезон доступны\n/cancle - что бы выбрать другой мультфильм")
    await UserState_RM.sezon.set()
"""Определение номера сезона и получение номера серии"""
@dp.message_handler(state=UserState_RM.sezon)
async def get_sezon_rick(message: types.Message, state: FSMContext):
    await state.update_data(sezon=message.text)
    username = message.from_user.username if message.from_user.username else None
    data = await state.get_data()
    sezon_number = data['sezon']
    if sezon_number == "1":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_RM.next()

    elif sezon_number == "2":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_RM.next()

    elif sezon_number == "3":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_RM.next()

    elif sezon_number == "4":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_RM.next()

    elif sezon_number == "5":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_RM.next()

    elif sezon_number == "/cancle":
        await state.finish()

    else:
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Такого сезона нет в базе!")
"""Обработка данных и отправка плользователю мультфильма"""
@dp.message_handler(state=UserState_RM.seriya)
async def get_seriya_rick(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else None
    await state.update_data(seriya=message.text)
    data = await state.get_data()
    try:
        cursor_mult.execute(f"SELECT * FROM rick_and_morty WHERE seriya = {data['seriya']} AND sezon = {data['sezon']};")
        cursor_tg.execute(f"SELECT * FROM rick_and_morty WHERE name_file = 'RM_{data['sezon']}_{data['seriya']}.mp4';")
        video_id_list = cursor_tg.fetchone()
        video_info_list = cursor_mult.fetchone()

        await message.answer(f"{video_info_list[0]}\nсезон:{video_info_list[2]} серия{video_info_list[1]}")
        await bot.send_video(message.from_user.id, video=video_id_list[1])
        logger.debug(f"{username} выбрал Сезон:{data['sezon']} Серию:{data['seriya']}")
        await state.finish()
    except:
        logger.warning(f"{username} данных нет в базе!")
        await message.answer("такого номера нет в базе, введите другой номер!")

class UserState_SP(StatesGroup):
    sezon = State()
    seriya = State()
"""Запрос на получение номера сезона"""
@dp.message_handler(commands="south_park")
async def write_db_video_rick(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    logger.debug(f"{username} выбрал Южный Парк")
    await message.answer("Выберите номер сезона\n1-25 Сезон доступны\n/cancle - что бы выбрать другой мультфильм")
    await UserState_SP.sezon.set()
"""Определение номера сезона и получение номера серии"""
@dp.message_handler(state=UserState_SP.sezon)
async def get_sezon_rick(message: types.Message, state: FSMContext):
    await state.update_data(sezon=message.text)
    username = message.from_user.username if message.from_user.username else None
    data = await state.get_data()
    sezon_number = data['sezon']
    if sezon_number == "1":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-13")
        await UserState_SP.next()

    elif sezon_number == "2":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-18")
        await UserState_SP.next()

    elif sezon_number == "3":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-17")
        await UserState_SP.next()

    elif sezon_number == "4":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-17")
        await UserState_SP.next()

    elif sezon_number == "5":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "6":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-17")
        await UserState_SP.next()

    elif sezon_number == "7":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-15")
        await UserState_SP.next()

    elif sezon_number == "8":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "9":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "10":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "11":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "12":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "13":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "14":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "15":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "16":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_SP.next()

    elif sezon_number == "17":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_SP.next()

    elif sezon_number == "18":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_SP.next()

    elif sezon_number == "19":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_SP.next()

    elif sezon_number == "20":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_SP.next()

    elif sezon_number == "21":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_SP.next()

    elif sezon_number == "22":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_SP.next()

    elif sezon_number == "23":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-10")
        await UserState_SP.next()

    elif sezon_number == "24":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-8")
        await UserState_SP.next()

    elif sezon_number == "25":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-6")
        await UserState_SP.next()

    elif sezon_number == "/cancle":
        await state.finish()

    else:
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Такого сезона нет в базе!")
"""Обработка данных и отправка плользователю мультфильма"""
@dp.message_handler(state=UserState_SP.seriya)
async def get_seriya_rick(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else None
    await state.update_data(seriya=message.text)
    data = await state.get_data()
    try:
        cursor_mult.execute(f"SELECT * FROM south_park WHERE seriya = {data['seriya']} AND sezon = {data['sezon']};")
        cursor_tg.execute(f"SELECT * FROM south_park WHERE name_file = 'SP_{data['sezon']}_{data['seriya']}.mp4';")
        video_id_list = cursor_tg.fetchone()
        video_info_list = cursor_mult.fetchone()

        await message.answer(f"{video_info_list[0]}\nсезон:{video_info_list[2]} серия{video_info_list[1]}")
        await bot.send_video(message.from_user.id, video=video_id_list[1])
        logger.debug(f"{username} выбрал Сезон:{data['sezon']} Серию:{data['seriya']}")
        await state.finish()
    except:
        logger.warning(f"{username} данных нет в базе!")
        await message.answer("такого номера нет в базе, введите другой номер!")


class UserState_AT(StatesGroup):
    sezon = State()
    seriya = State()
"""Запрос на получение номера сезона"""
@dp.message_handler(commands="adventure_time")
async def write_db_video_rick(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    logger.debug(f"{username} выбрал Время Приключений")
    await message.answer("Выберите номер сезона\n1-10 Сезон доступны\n/cancle - что бы выбрать другой мультфильм")
    await UserState_AT.sezon.set()
"""Определение номера сезона и получение номера серии"""
@dp.message_handler(state=UserState_AT.sezon)
async def get_sezon_rick(message: types.Message, state: FSMContext):
    await state.update_data(sezon=message.text)
    username = message.from_user.username if message.from_user.username else None
    data = await state.get_data()
    sezon_number = data['sezon']
    if sezon_number == "1":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-26")
        await UserState_AT.next()

    elif sezon_number == "2":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-26")
        await UserState_AT.next()

    elif sezon_number == "3":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-25")
        await UserState_AT.next()

    elif sezon_number == "4":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-26")
        await UserState_AT.next()

    elif sezon_number == "5":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-51")
        await UserState_AT.next()

    elif sezon_number == "6":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-43")
        await UserState_AT.next()

    elif sezon_number == "7":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-38")
        await UserState_AT.next()

    elif sezon_number == "8":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_AT.next()

    elif sezon_number == "9":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-14")
        await UserState_AT.next()

    elif sezon_number == "10":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-13")
        await UserState_AT.next()

    elif sezon_number == "/cancle":
        await state.finish()

    else:
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Такого сезона нет в базе!")
"""Обработка данных и отправка плользователю мультфильма"""
@dp.message_handler(state=UserState_AT.seriya)
async def get_seriya_rick(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else None
    await state.update_data(seriya=message.text)
    data = await state.get_data()
    try:
        cursor_mult.execute(f"SELECT *FROM adventure_time WHERE seriya = {data['seriya']} AND sezon = {data['sezon']};")
        cursor_tg.execute(f"SELECT * FROM adventure_time WHERE name_file = 'AT_{data['sezon']}_{data['seriya']}.mp4';")
        video_id_list = cursor_tg.fetchone()
        video_info_list = cursor_mult.fetchone()

        await message.answer(f"{video_info_list[0]}\nсезон:{video_info_list[2]} серия{video_info_list[1]}")
        await bot.send_video(message.from_user.id, video=video_id_list[1])
        logger.debug(f"{username} выбрал Сезон:{data['sezon']} Серию:{data['seriya']}")
        await state.finish()
    except:
        logger.warning(f"{username} данных нет в базе!")
        await message.answer("такого номера нет в базе, введите другой номер!")


class UserState_LDR(StatesGroup):
    sezon = State()
    seriya = State()
"""Запрос на получение номера сезона"""
@dp.message_handler(commands="love_death_and_robots")
async def write_db_video_rick(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    logger.debug(f"{username} выбрал Любовь Смерть и Роботы")
    await message.answer("Выберите номер сезона\n1-3 Сезон доступны\n/cancle - что бы выбрать другой мультфильм")
    await UserState_LDR.sezon.set()
"""Определение номера сезона и получение номера серии"""
@dp.message_handler(state=UserState_LDR.sezon)
async def get_sezon_rick(message: types.Message, state: FSMContext):
    await state.update_data(sezon=message.text)
    username = message.from_user.username if message.from_user.username else None

    data = await state.get_data()
    sezon_number = data['sezon']

    if sezon_number == "1":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-18")
        await UserState_LDR.next()

    elif sezon_number == "2":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-8")
        await UserState_LDR.next()

    elif sezon_number == "3":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-9")
        await UserState_LDR.next()

    elif sezon_number == "/cancle":
        await state.finish()

    else:
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Такого сезона нет в базе!")
"""Обработка данных и отправка плользователю мультфильма"""
@dp.message_handler(state=UserState_LDR.seriya)
async def get_seriya_rick(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else None
    await state.update_data(seriya=message.text)
    data = await state.get_data()
    try:
        cursor_mult.execute(f"SELECT * FROM love_death_and_robots WHERE seriya = {data['seriya']} AND sezon = {data['sezon']};")
        cursor_tg.execute(f"SELECT * FROM love_death_and_robots WHERE name_file = 'LDR_{data['sezon']}_{data['seriya']}.mp4';")
        video_id_list = cursor_tg.fetchone()
        video_info_list = cursor_mult.fetchone()

        await message.answer(f"{video_info_list[0]}\nсезон:{video_info_list[2]} серия{video_info_list[1]}")
        await bot.send_video(message.from_user.id, video=video_id_list[1])
        logger.debug(f"{username} выбрал Сезон:{data['sezon']} Серию:{data['seriya']}")
        await state.finish()
    except:
        logger.warning(f"{username} данных нет в базе!")
        await message.answer("такого номера нет в базе, введите другой номер!")


class UserState_WBB(StatesGroup):
    sezon = State()
    seriya = State()
"""Запрос на получение номера сезона"""
@dp.message_handler(commands="we_bare_bears")
async def write_db_video_wbb(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    logger.debug(f"{username} выбрал Мы Обычные Медведи")
    await message.answer("Выберите номер сезона\n1-3 Сезон доступны\n/cancle - что бы выбрать другой мультфильм")
    await UserState_WBB.sezon.set()
"""Определение номера сезона и получение номера серии"""
@dp.message_handler(state=UserState_WBB.sezon)
async def get_sezon_wbb(message: types.Message, state: FSMContext):
    await state.update_data(sezon=message.text)
    username = message.from_user.username if message.from_user.username else None
    data = await state.get_data()
    sezon_number = data['sezon']

    if sezon_number == "1":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-26")
        await UserState_WBB.next()

    elif sezon_number == "2":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-25")
        await UserState_WBB.next()

    elif sezon_number == "3":
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Выберите серию 1-44")
        await UserState_Wbb.next()

    elif sezon_number == "/cancle":
        await state.finish()

    else:
        logger.debug(f"{username} ввёл номер сезона {sezon_number}")
        await message.answer("Такого сезона нет в базе!")
"""Обработка данных и отправка плользователю мультфильма"""
@dp.message_handler(state=UserState_WBB.seriya)
async def get_seriya_wbb(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else None
    await state.update_data(seriya=message.text)
    data = await state.get_data()
    try:
        cursor_mult.execute(f"SELECT * FROM we_bare_bears WHERE seriya = {data['seriya']} AND sezon = {data['sezon']};")
        cursor_tg.execute(f"SELECT * FROM we_bare_bears WHERE name_file = 'WBB_{data['sezon']}_{data['seriya']}.mp4';")
        video_id_list = cursor_tg.fetchone()
        video_info_list = cursor_mult.fetchone()

        await message.answer(f"{video_info_list[0]}\nсезон:{video_info_list[2]} серия{video_info_list[1]}")
        await bot.send_video(message.from_user.id, video=video_id_list[1])
        logger.debug(f"{username} выбрал Сезон:{data['sezon']} Серию:{data['seriya']}")
        await state.finish()
    except:
        logger.warning(f"{username} данных нет в базе!")
        await message.answer("такого номера нет в базе, введите другой номер!")

def start_bot():
    executor.start_polling(dp, skip_updates=True)
