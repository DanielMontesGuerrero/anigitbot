import requests
import random

API_URL = 'https://api.waifu.pics'

categories = {
    'sfw': [
        'waifu',
        'neko',
        'shinobu',
        'megumin',
        'bully',
        'cuddle',
        'cry',
        'hug',
        'awoo',
        'kiss',
        'lick',
        'pat',
        'smug',
        'bonk',
        'yeet',
        'blush',
        'smile',
        'wave',
        'highfive',
        'handhold',
        'nom',
        'bite',
        'glomp',
        'slap',
        'kill',
        'kick',
        'happy',
        'wink',
        'poke',
        'dance',
        'cringe',
    ],
    'nswf': [
        'waifu',
        'neko',
        'trap',
        'blowjob',
    ],
}

def get_random_waifu(nsfw: bool = False) -> str:
    waifu_type = 'sfw'
    if nsfw:
        waifu_type = 'nsfw'
    index = random.randint(0, len(categories[waifu_type]) - 1)
    category = categories[waifu_type][index]
    res = requests.get(f'{API_URL}/{waifu_type}/{category}')
    data = res.json()
    return data['url']
