import requests
import os
from os import listdir
import telegram
from time import sleep
import random
from argparse import unquote
from datetime import datetime
from urllib.parse import urlparse


def download_picture(url, path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def extract_format_from_link(link):
    decoding_link = unquote(link)
    parse_link = urlparse(decoding_link)
    path, fullname = os.path.split(parse_link.path)
    format_path = os.path.splitext(fullname)
    file_name, format = format_path
    return format, file_name


def main():
    EPIC_nasa(5)
    os.makedirs("images", exist_ok=True)
    telegram_token = os.environ['TG_TOKEN']
    time = os.environ["TIME_REPEAT"]
    time_repeat = os.environ.get(time, 14400)
    telegram_id = os.environ["TG_CHAT_ID"]
    bot = telegram.Bot(token=telegram_token)
    while True:
        files = "images"
        file = listdir(files)
        random.shuffle(file)
        for image in file:
            filepath = os.path.join(files, image)
            with open(filepath, "rb") as f:
                bot.send_document(chat_id=telegram_id, document=f)
        sleep(time_repeat)


if __name__ == "__main__":
    main()
