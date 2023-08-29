import requests
import argparse
from download_picture import download_picture


def fetch_spacex_last_launch(launch_id=None):
    if launch_id:
        url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    else:
        url = "https://api.spacexdata.com/v5/launches/"
    response = requests.get(url)
    response.raise_for_status()

    for response_link in response.json():
        if response_link["links"]["flickr"]["original"]:
            url_photos = response_link["links"]["flickr"]["original"]
            for number, url_photo in enumerate(url_photos):
                filename = f"images/spacex{number}.jpg"
                download_picture(url_photo, filename)


def main():
    parser = argparse.ArgumentParser(
    description="ID запуска"
)
    parser.add_argument('--id', default=None, help='ID', dest="ID")
    args = parser.parse_args()
    fetch_spacex_last_launch(args.ID)
if __name__ == "__main__":
    main()
