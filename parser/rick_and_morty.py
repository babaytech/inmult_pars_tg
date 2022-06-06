###################################################
import sqlite3
import json
import colorama
import requests
from bs4 import BeautifulSoup
###################################################


def progress_bar(progress, total, color=colorama.Fore.LIGHTYELLOW_EX):
        percent = 100 * (progress / float(total))
        print(color + f"\rПарсинг Южного Парка... | {percent:.2f}%", end="")
        if progress == total:
            print(colorama.Fore.GREEN + f"\rПарсинг Южного Парка завершён | {percent:.2f}%",end="")

def main_mult():
    print(colorama.Fore.RED + "====================\nРик и Морти запуск парсинга\n====================")

    # иницилизация хендлера и прокси
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    proxies = {'http': 'http://67.212.186.101:80'}

    sezon = 0
    database_list = []
    # цикл для смены страницы
    for i in range(5):
        seriya = 1
        sezon += 1
        url = f'https://rickandmorty.cn-fan.tv/season.php?id={sezon}'
        request = requests.get(url, headers=headers, proxies=proxies)
        root = BeautifulSoup(request.text, 'lxml')
        div = root.find('div', id='descrSeason')
        table = div.find('table')
        tds = table.find_all('h2')
        # проход по все странице
        for td in tds:
            cards_seriya = td.find_all('a')
            for card_seriya in cards_seriya:
                database_list_time = []
                a_link = card_seriya.get('href')
                clear_url = f'https://rickandmorty.cn-fan.tv/{a_link}'
                res = requests.get(clear_url, headers=headers, proxies=proxies)
                soup_seriya = BeautifulSoup(res.text, 'lxml')
                title_seriya = soup_seriya.find('h1').text.strip()
                url_mp4_seriya = soup_seriya.find('div', id="centerSeries").find('script', type="text/javascript").text.strip()
                seriya_mp4 = url_mp4_seriya.split("'")[5]
                database_list_time.append(title_seriya)
                database_list_time.append(seriya)
                database_list_time.append(sezon)
                database_list_time.append(seriya_mp4)
                database_list.append(database_list_time)
                print(colorama.Fore.BLUE + f"{database_list_time}")
                seriya += 1

    # Запись в базу данных
    print(colorama.Fore.GREEN + "====================\nРик и Морти записан в базу данных\n====================")
    conn = sqlite3.connect('serial.sqlite3')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rick_and_morty")
    cursor.executemany("INSERT INTO rick_and_morty VALUES(?, ?, ?, ?);", database_list)
    conn.commit()
    conn.close()
    print(colorama.Fore.RESET)