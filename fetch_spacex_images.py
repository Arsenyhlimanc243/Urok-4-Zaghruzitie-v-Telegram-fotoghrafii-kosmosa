import requests
import argparse
from download_picture import download_picture


def fetch_spacex_last_launch():
    for response_link in response.json():
        if response_link["links"]["flickr"]["original"]:
            url_photos = response_link["links"]["flickr"]["original"]
            for number, url_photo in enumerate(url_photos):
                filename = f"images/spacex{number}.jpg"
                download_picture(url_photo, filename)


def main():
     parser = argparse.ArgumentParser(description="Этот скрипт загружает фото от SpaceX по указанному ID запуска")
     parser.add_argument('--id', default=None, help='ID запуска, по которому загружается фото от SpaceX', dest="ID")
     args = parser.parse_args()
     if launch_id=None:
          url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
     else:
          url = "https://api.spacexdata.com/v5/launches/"
     response = requests.get(url)
     response.raise_for_status()
     fetch_spacex_last_launch(args.ID)


if __name__ == "__main__":
    main()
