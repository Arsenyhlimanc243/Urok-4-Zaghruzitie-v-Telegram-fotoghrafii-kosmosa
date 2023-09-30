import requests
import os
from os import listdir
import telegram
from time import sleep
import random
from argparse import unquote
from datetime import datetime
from urllib.parse import urlparse


def main():
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
