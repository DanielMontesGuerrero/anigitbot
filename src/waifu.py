import requests
import random
import json

from typing import Dict, Tuple


def get_random_waifu(nsfw: bool = False) -> str:
    API_URL, categories = get_config()
    waifu_type = 'sfw'
    if nsfw:
        waifu_type = 'nsfw'
    index = random.randint(0, len(categories[waifu_type]) - 1)
    category = categories[waifu_type][index]
    res = requests.get(f'{API_URL}/{waifu_type}/{category}')
    data = res.json()
    return data['url']

def get_config() -> Tuple[str, Dict]:
    with open(f'{__file__[:-8]}/config.json') as json_file:
        data = json.load(json_file)
        url = data['url']
        categories = data['categories']
        return url, categories
