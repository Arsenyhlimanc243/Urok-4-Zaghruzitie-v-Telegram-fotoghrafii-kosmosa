import requests
import os
from urllib.parse import urlparse, unquote
from download_picture import download_picture


def extract_format_from_link(link):
    decoding_link = unquote(link)
    parse_link = urlparse(decoding_link)
    path, fullname = os.path.split(parse_link.path)
    format_path = os.path.splitext(fullname)
    file_name, format = format_path
    return format, file_name


def nasa_get(images):
    api_key = os.environ['API_KEY']
    payload = {
        "api_key": api_key,
        "count": images
    }
    response = requests.get("https://api.nasa.gov/planetary/apod", params=payload)
    response.raise_for_status()
    images = response.json()
    for image in images:
        if image.get("media_type") == "image":
            if image.get("hdurl"):
                url_photo = image["hdurl"]
            else:
                url_photo = image["url"]
            format, file_name = extract_format_from_link(url_photo)
            path = os.path.join("image", f"{file_name}{format}")
            download_picture(url_photo, path, params=payload)


def main():
    nasa_get(30)


if "__main__" == "__name__":
    main()

