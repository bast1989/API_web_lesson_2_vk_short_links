from urllib.parse import urlparse

import decouple
import requests
from decouple import config


def shorten_link(token, url):
    shortlink_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'v': '5.199',
        'access_token': token,
        'private': '0',
        'url': url
    }
    response = requests.get(shortlink_url, params=params)
    response.raise_for_status()
    short_link = response.json()
    return short_link['response']['short_url']


def count_clicks(token, link):
    clickstats_url = 'https://api.vk.ru/method/utils.getLinkStats'
    short_path = urlparse(link).path.lstrip('/')
    params = {
        'v': '5.199',
        'access_token': token,
        'interval': 'forever',
        'key': short_path
    }
    response = requests.get(clickstats_url, params=params)
    response.raise_for_status()
    link_clicks = response.json()
    return link_clicks['response']['stats'][0]['views']


def is_shorten_link(url):
    is_shorten = True
    parsed = urlparse(url)
    if parsed.netloc not in 'vk.cc':
        is_shorten = False
    return is_shorten


def main():
    try:
        vk_token = config('TOKEN')
        link = input('Введите ссылку: ')
        is_shorten = is_shorten_link(link)
        if is_shorten:
            print(f'Количество посещений: {count_clicks(vk_token, link)}')
        else:
            print(f'Сокращенная ссылка: {shorten_link(vk_token, link)}')
    except requests.exceptions.HTTPError as err:
        print(f'Произошла ошибка: {err}')
        print('Проверьте опечатки в адресе сайта')
    except decouple.UndefinedValueError as err:
        print(f'Произошла ошибка: {err}')
        print('Переменная окружения/в .env не найдена')
    except requests.exceptions.ConnectionError as err:
        print(f'Произошла ошибка: {err}')
        print('Проверьте сетевое подключение или его настройки')


if __name__ == '__main__':
    main()