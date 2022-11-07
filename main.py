import os
import requests

from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
from urllib.parse import unquote


def compile_comix_url(comix_id):
    xkcd_url = "https://xkcd.com/"
    comix_url = f"{xkcd_url}{comix_id}/info.0.json"
    return comix_url


def get_comix_meta(url):
    repsonse = requests.get(url)
    repsonse.raise_for_status()
    return repsonse.json()


def compose_filepath(url):
    url_part = urlparse(url).path
    unquoted_url_part = unquote(url_part)
    name = os.path.split(unquoted_url_part)[-1]
    return Path(f"./{name}")


def save_content(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, "wb") as file:
        file.write(response.content)
        return path


def fetch_comix():
    comix_id = 353
    comix_url = compile_comix_url(comix_id)
    comix_meta = get_comix_meta(comix_url)
    image_url = comix_meta["img"]
    image_path = compose_filepath(image_url)
    image = save_content(image_url, image_path)
    text = comix_meta["alt"]
    return image, text


def get_upload_url(api_url, params):
    method = "photos.getWallUploadServer"
    method_url = f"{api_url}method/{method}"
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_to_server(upload_url, image):
    with open(image, "rb") as file:
        method = "photos.saveWallPhoto"
        files = {
            "photo": file,
        }
        method_url = f"{upload_url}{method}"
        response = requests.post(method_url, files=files)
        response.raise_for_status()
        return response.json()


def save_to_album(api_url, params, upload_response):
    method = "photos.saveWallPhoto"
    params = params | upload_response
    method_url = f"{api_url}method/{method}"
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    return response.json()


def post_to_the_wall(api_url, params, save_response, group_id, text):
    method = "wall.post"
    method_url = f"{api_url}method/{method}"
    owner_id = save_response["response"][0]["owner_id"]
    media_id = save_response["response"][0]["id"]
    params["owner_id"] = f"-{group_id}"
    params["message"] = text
    params["from_group"] = 1
    params["attachments"] = f"photo{owner_id}_{media_id}"
    response = requests.get(method_url, params=params)
    response.raise_for_status()


def publish_to_vk(group_id, token, image, text):
    api_url = "https://api.vk.com/"
    api_version = 5.131
    params = {
        "access_token": token,
        "v": api_version,
    }
    upload_url = get_upload_url(api_url, params)
    upload_response = upload_to_server(upload_url, image)
    save_response = save_to_album(api_url, params, upload_response)
    post_to_the_wall(api_url, params, save_response, group_id, text)


def main():
    load_dotenv()
    group_id = os.getenv("VK_GROUP_ID")
    token = os.getenv("VK_ACCESS_TOKEN")
    image, text = fetch_comix()
    publish_to_vk(group_id, token, image, text)


if __name__ == "__main__":
    main()
