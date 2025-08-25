import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN = os.getenv('TOKEN')


def shorten_link(token, url):
    url_method = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'v': '5.199',
        'access_token': token,
        'private': '0',
        'url': url
    }
    response = requests.get(url_method, params=params)
    response.raise_for_status()
    short_link = response.json()
    return short_link['response']['short_url']


def count_clicks(token, link):
    url_method = 'https://api.vk.ru/method/utils.getLinkStats'
    body_link = urlparse(link).path.lstrip('/')
    params = {
        'v': '5.199',
        'access_token': token,
        'interval': 'forever',
        'key': body_link
    }
    response = requests.get(url_method, params=params)
    response.raise_for_status()
    view_link = response.json()
    return view_link['response']['stats'][0]['views']


def is_shorten_link(url):
    is_shorten = True
    parsed = urlparse(url)
    if parsed.netloc not in 'vk.cc':
        is_shorten = False
    return is_shorten


def main():
    try:
        link = input('Введите ссылку: ')
        is_shorten = is_shorten_link(link)
        if is_shorten:
            print(f'Количество посещений: {count_clicks(VK_TOKEN, link)}')
        else:
            print(f'Сокращенная ссылка: {shorten_link(VK_TOKEN, link)}')
    except requests.exceptions.HTTPError as err:
        print(f'Произошла ошибка: {err}')
        print('Проверьте опечатки в адресе сайта')
    except Exception as err:
        print(f'Произошла ошибка: {err}')


if __name__ == '__main__':
    main()