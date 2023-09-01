import logging

import requests
import time

from urllib.parse import urlparse, parse_qs

from config import YOUTUBE_RSS_URL, YOUTUBE_API_KEY
from database import load_db, update_new_obj

from rss_helper import RSSHelper

rsh = RSSHelper()

# URL для проверки существования канала
CHANNEL_URL = 'https://www.googleapis.com/youtube/v3/channels'


def get_all_urls_from_rss(rss_feed):
    links = rsh.get_rss_links(rss_feed)
    return links


def check_new_item(old_list: list, new_list: list):
    old_set = set(old_list)
    new_set = set(new_list)

    # Calculate the items that are in new_list but not in old_list
    new_items = list(new_set - old_set)

    return new_items


def get_all_new_links():
    new_writing_dict = {}
    data = load_db()
    new_links = []
    for key in data:
        urls: list = get_all_urls_from_rss(YOUTUBE_RSS_URL + key)
        new_items: list = check_new_item(data[key], urls)
        new_links += new_items
        new_writing_dict.update({key: urls})
        time.sleep(0.05)
    update_new_obj(new_writing_dict)
    return new_links


def extract_channel_id(url):
    # Разбираем URL
    parsed_url = urlparse(url)

    # Проверяем, является ли URL адресом канала в формате /channel/
    if "/channel/" in parsed_url.path:
        # Извлекаем идентификатор канала из URL
        channel_id = parsed_url.path.split("/channel/")[1]
        return channel_id, None

    # Проверяем, является ли URL адресом вида /@username
    if parsed_url.path.startswith("/@"):
        username = parsed_url.path[2:]
        return None, username

    # Если не удалось извлечь идентификатор канала, возвращаем None
    return None, None


def validate_channel(url) -> (bool, str):
    channel_id, username = extract_channel_id(url)
    params = {
        "part": "snippet",
        'key': YOUTUBE_API_KEY,
        "id": channel_id
    }
    if username:
        return False, None
    try:
        response = requests.get(CHANNEL_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                channel_info = data['items'][0]
                return True, channel_info['snippet']['title']
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    return False, None
