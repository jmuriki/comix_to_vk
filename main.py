import os
import random
import requests

from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
from urllib.parse import unquote


def fetch_random_comic():
    url = "https://xkcd.com/"
    info_path = "/info.0.json"
    response = requests.get(f"{url}{info_path}")
    response.raise_for_status()
    total_comics = response.json()["num"]
    comic_id = random.randint(1, total_comics)
    response = requests.get(f"{url}{comic_id}{info_path}")
    response.raise_for_status()
    comic_meta = response.json()
    image_url = comic_meta["img"]
    image_alt = comic_meta["alt"]
    return image_url, image_alt


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


def check_for_vk_error(response):
    error = response.json().get("error")
    if error:
        code = error.get("error_code")
        msg = error["error_msg"]
        return f"[VK Error: {code}] {msg}" if code else msg
    return


def get_upload_url(api_url, token, api_version):
    method = "photos.getWallUploadServer"
    method_url = f"{api_url}method/{method}"
    params = {
        "access_token": token,
        "v": api_version,
    }
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    error = check_for_vk_error(response)
    if error:
        raise requests.HTTPError(error)
    return response.json()["response"]["upload_url"]


def upload_to_server(upload_url, image):
    method = "photos.saveWallPhoto"
    method_url = f"{upload_url}{method}"
    with open(image, "rb") as file:
        files = {
            "photo": file,
        }
        response = requests.post(method_url, files=files)
    response.raise_for_status()
    error = check_for_vk_error(response)
    if error:
        raise requests.HTTPError(error)
    return response.json()


def save_to_album(api_url, token, api_version, img_server, img_photo, img_hash):
    method = "photos.saveWallPhoto"
    method_url = f"{api_url}method/{method}"
    params = {
        "access_token": token,
        "v": api_version,
        "server": img_server,
        "photo": img_photo,
        "hash": img_hash,
    }
    response = requests.post(method_url, params=params)
    response.raise_for_status()
    error = check_for_vk_error(response)
    if error:
        raise requests.HTTPError(error)
    return response.json()


def post_to_the_wall(api_url, token, api_version, owner_id, media_id, group_id, image_alt):
    method = "wall.post"
    method_url = f"{api_url}method/{method}"
    params = {
        "access_token": token,
        "v": api_version,
        "owner_id": f"-{group_id}",
        "message": image_alt,
        "from_group": 1,
        "attachments": f"photo{owner_id}_{media_id}",
    }
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    error = check_for_vk_error(response)
    if error:
        raise requests.HTTPError(error)


def publish_to_vk(group_id, token, image, image_alt):
    api_url = "https://api.vk.com/"
    api_version = 5.131
    upload_url = get_upload_url(
        api_url,
        token,
        api_version,
    )
    upload_response = upload_to_server(upload_url, image)
    img_server = upload_response["server"]
    img_photo = upload_response["photo"]
    img_hash = upload_response["hash"]
    save_response = save_to_album(
        api_url,
        token,
        api_version,
        img_server,
        img_photo,
        img_hash,
    )
    owner_id = save_response["response"][0]["owner_id"]
    media_id = save_response["response"][0]["id"]
    post_to_the_wall(
        api_url,
        token,
        api_version,
        owner_id,
        media_id,
        group_id,
        image_alt,
    )


def main():
    load_dotenv()
    group_id = os.getenv("VK_GROUP_ID")
    token = os.getenv("VK_ACCESS_TOKEN")
    image_url, image_alt = fetch_random_comic()
    image_path = compose_filepath(image_url)
    try:
        save_content(image_url, image_path)
        publish_to_vk(group_id, token, image_path, image_alt)
    except requests.HTTPError:
        raise
    finally:
        os.remove(image_path)


if __name__ == "__main__":
    main()
