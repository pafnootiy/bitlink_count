import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse


def shorten_link(headers, url):
    url_shorten = "https://api-ssl.bitly.com/v4/shorten"
    data = {
        "long_url": url,
    }
    response = requests.post(url_shorten, headers=headers, json=data)
    response.raise_for_status()
    response_json = response.json()
    return response_json.get("id")


def count_clicks(headers, url):
    url_parsed = urlparse(url)
    if url != url_parsed.path:
        url = f"{url_parsed.hostname}{url_parsed.path}"
    url_for_count = f"https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary"
    params = {
        'unit': '',
        'units': '-1',
    }
    response = requests.get(url_for_count, headers=headers, params=params)
    response.raise_for_status()
    clicks = response.json()
    return clicks.get("total_clicks")


def is_bitlink(url, headers):
    url_parsed = urlparse(url)
    if url != url_parsed.path:
        url = f"{url_parsed.netloc}{url_parsed.path}"
    url_for_bitlink = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    response = requests.get(url_for_bitlink, headers=headers)
    return response.ok


def createParser():
    parser = argparse.ArgumentParser(description='Create bitlink or count bitlink')
    parser.add_argument("url_path")
    return parser


def main():
    load_dotenv()
    token = os.getenv("BITLINK_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    parser = createParser()
    namespace = parser.parse_args()
    url = namespace.url_path


    try:
        if is_bitlink(url, headers):
            print("Количество переходов по ссылке:",
                  count_clicks(headers, url))
        else:
            print('Битлинк', shorten_link(headers, url))
    except requests.exceptions.HTTPError:
        print("Где то ошибка ,исправь")


if __name__ == "__main__":
    main()
