import requests

from pathlib import Path
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


def main():
    comix_id = 353
    url = f"https://xkcd.com/{comix_id}/info.0.json"
    comix_meta = get_comix_meta(url)
    img_url = comix_meta["img"]
    img_path = compose_filepath(img_url)
    save_content(img_url, img_path)
    print(comix_meta["alt"])


if __name__ == "__main__":
    main()
