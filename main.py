import os
import requests

from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
from urllib.parse import unquote


def get_comix_meta(url):
    repsonse = requests.get(url)
    repsonse.raise_for_status()
    return repsonse.json()


def compose_filepath(url):
    url_part = urlparse(url).path
    unquoted_url_part = unquote(url_part)
    name = os.path.split(unquoted_url_part)[-1]
    return f"./{name}"


def save_content(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(Path(path), "wb") as file:
        file.write(response.content)


def fetch_comix():
    xkcd_url = "https://xkcd.com/"
    comix_id = 353
    comix_url = f"{xkcd_url}{comix_id}/info.0.json"
    comix_meta = get_comix_meta(comix_url)
    img_url = comix_meta["img"]
    img_path = compose_filepath(img_url)
    save_content(img_url, img_path)
    print(comix_meta["alt"])
    return img_path


def get_upload_url(api_url, params):
    method = "photos.getWallUploadServer"
    method_url = f"{api_url}method/{method}"
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_to_server(upload_url, group_id, pic_path):
    with open(Path(pic_path), "rb") as file:
        method = "photos.saveWallPhoto"
        files = {
            "photo": file,
        }
        params = {
            "group_id": group_id,
        }
        method_url = f"{upload_url}{method}"
        response = requests.post(method_url, files=files, params=params)
        response.raise_for_status()
    return response.json()


def save_to_album(api_url, params, upload_response):
    method = "photos.saveWallPhoto"
    params = params | upload_response
    method_url = f"{api_url}method/{method}"
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    print(response.json())


def main():
    load_dotenv()
    access_token = os.getenv("VK_ACCESS_TOKEN")
    group_id = os.getenv("VK_GROUP_ID")
    api_url = "https://api.vk.com/"
    api_version = 5.131
    params = {
        "access_token": access_token,
        "v": api_version,
    }
    pic_path = fetch_comix()
    upload_url = get_upload_url(api_url, params)
    upload_response = upload_to_server(upload_url, group_id, pic_path)
    save_to_album(api_url, params, upload_response)


if __name__ == "__main__":
    main()
