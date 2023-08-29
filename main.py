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


def fetch_spacex_last_launch():
    url = "https://api.spacexdata.com/v5/launches/"
    response = requests.get(url)
    response.raise_for_status()
    for response_link in response.json():
        if response_link["links"]["flickr"]["original"]:
            url_photos = response_link["links"]["flickr"]["original"]
            for number, url_photo in enumerate(url_photos):
                filename = f"images/spacex{number}.jpg"
            download_picture(url_photo, filename)


def extract_format_from_link(link):
    decoding_link = unquote(link)
    parse_link = urlparse(decoding_link)
    path, fullname = os.path.split(parse_link.path)
    format_path = os.path.splitext(fullname)
    file_name, format = format_path
    return format, file_name


def nasa_get(images):
    payload = {
        "api_key": "2ov0b0AG8Q5WzcSz571mYwUK8h3WHg6WsX2J2Q1j",
        "count": images
    }
    response = requests.get("https://api.nasa.gov/planetary/apod",
                            params=payload)
    response.raise_for_status()
    images_json = response.json()
    for image_json in images_json:
        if image_json.get("media_type") == "image":
            if image_json.get("hdurl"):
                url_photos = image_json["hdurl"]
            else:
                url_photos = image_json["url"]
            format, file_name = extract_format_from_link(url_photos)
            path = os.path.join("images", f"{file_name}{format}")
            download_picture(url_photos, path, params=payload)


def EPIC_nasa(images):
    params = {
        "api_key": "2ov0b0AG8Q5WzcSz571mYwUK8h3WHg6WsX2J2Q1j",
        "count": images,
    }
    response = requests.get("https://api.nasa.gov/EPIC/api/natural/image",
                            params=params)
    response.raise_for_status()
    url_json = response.json()
    for image_url in url_json:
        image_urls = image_url["image"]
        image_date = image_url["date"]
        image_date = datetime.fromisoformat(image_date).strftime("%Y/%m/%d")
        new_url = f"https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_urls}.png"
        print(new_url)
        path = os.path.join("images", f"{image_urls}.png")
        download_picture(new_url, path, params)


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
        sleep(int(str(time_repeat)))


if __name__ == "__main__":
    main()
