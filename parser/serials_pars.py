import sqlite3
import colorama
import requests
from bs4 import BeautifulSoup

def main_inter_serials():
    page = 1
    database_list = []
    conn = sqlite3.connect('serial.sqlite3')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM serials")

    def progress_bar(progress, total, color=colorama.Fore.LIGHTYELLOW_EX):
        percent = 100 * (progress / float(total))
        print(color + f"\rПарсинг фильмов... | {percent:.2f}% | страница:{page}/188", end="")
        if progress == total:
            print(colorama.Fore.GREEN + f"\rПарсинг аниме завершён | {percent:.2f}% | страница:{page}/188", end="")

    for i in range(188):
        url = f'https://lordserial.site/zarubezhnye-serialy/page/{page}/'
        request = requests.get(url)
        root = BeautifulSoup(request.text, 'lxml')
        main_serial = root.find('div', class_="sect-cont sect-items clearfix")
        serials = main_serial.find_all('div', class_="th-item")
        for serial in serials:
            database_list_time = []
            title_serial = serial.find('div', class_="th-title")
            year_serial = serial.find('div', class_="th-year")
            series_serial = serial.find('div', class_="th-series")
            url_serial = serial.find('a', class_="th-in with-mask").get('href')
            database_list_time.append(title_serial.text)
            database_list_time.append(year_serial.text)
            database_list_time.append(series_serial.text)
            database_list_time.append(url_serial)
            database_list.append(database_list_time)
        progress_bar(i + 1, 188)
        # system('cls')
        page += 1
    cursor.executemany("INSERT INTO serials VALUES(?, ?, ?, ?);", database_list)
    conn.commit()
    print(colorama.Fore.RESET)
