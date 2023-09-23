from download_picture import download_picture
import requests
import os
from datetime import datetime


def epic_nasa(images):
    api_key = os.environ['API_KEY']
    params = {
        "api_key": api_key,
        "count": images,
    }
    response = requests.get("https://api.nasa.gov/EPIC/api/natural/image", params=params)
    response.raise_for_status()
    url = response.json()
    for image_urls in url:
        image_url = image_urls["image"]
        image_date = image_urls["date"]
        image_date = datetime.fromisoformat(image_date).strftime("%Y/%m/%d")
        new_url = f"https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_url}.png"
        path = os.path.join("images", f"{image_url}.png")
        download_picture(new_url, path, params)


def main():
    epic_nasa(5)


if "__main__" == "__name__":
    main()
