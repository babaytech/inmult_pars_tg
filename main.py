#####################################################################
import configparser
import sqlite3
import bot.bot
import colorama
#####################################################################


print(colorama.Fore.RED + " _____                         _               _            _     ")
print(colorama.Fore.RED + "/  ___|                       (_)             | |          | |    ")
print(colorama.Fore.RED + "\ `--.  __ _ _ __   __ _ _   _ _ _ __   ___   | |_ ___  ___| |__  ")
print(colorama.Fore.RED + " `--. \/ _` | '_ \ / _` | | | | | '_ \ / _ \  | __/ _ \/ __| '_ \ ")
print(colorama.Fore.RED + "/\__/ / (_| | | | | (_| | |_| | | | | |  __/  | ||  __/ (__| | | |")
print(colorama.Fore.RED + "\____/ \__,_|_| |_|\__, |\__,_|_|_| |_|\___|   \__\___|\___|_| |_|")
print(colorama.Fore.RED + "                    __/ |                                         ")
print(colorama.Fore.RED + "                   |___/                                          ")
print(colorama.Fore.RESET)

config = configparser.ConfigParser()
config.read('config.ini')

conn = sqlite3.connect('serial.sqlite3')
cursor = conn.cursor()

if __name__ == '__main__':
    print(config["DEFAULT"]["version"])
    bot.bot.start_bot()
    conn.close()