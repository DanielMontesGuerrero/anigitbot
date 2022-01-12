from dataclasses import fields
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import asyncio
from github3 import github
from hikari.embeds import Embed
import requests
import json
from anigitbot import Anigitrest
from github_handler import GithubHandler
from utils import get_pr_embed

class Handler(BaseHTTPRequestHandler):
    def __init__(self, discord_token, github_token, *args, **kwargs):
        self.github_token = github_token
        self.discord_token = discord_token
        super().__init__(*args, **kwargs)

    def do_GET(self):
        data = urllib.parse.parse_qs(self.path[2:])
        print(data)
        channel_id = int(data['channel_id'][0])
        user = data['user'][0]
        repository_name = data['repo'][0]
        pr_number = int(data['pr'][0])
        self.notify_pull_request(channel_id, user, repository_name, pr_number)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Done"
        self.wfile.write(bytes(message, "utf8"))

    def notify_pull_request(self, channel_id, user, repository_name, pr_number):
        github = GithubHandler(self.github_token)
        pr = github.get_pull_request(user, repository_name, pr_number)
        embed = get_pr_embed(pr)
        self.send_to_discord(channel_id, embed)

    def to_dict(self, embed: Embed):
        fields = [
            {
                'name': item.name,
                'value': item.value,
            }
            for item in embed.fields
        ]
        parsed_embed = {
            'title': embed.title,
            'url': embed.url,
            'description': embed.description,
            'color': embed.color,
            'thumbnail': {
                'url': embed.thumbnail.url,
            },
            'image': {
                'url': embed.image.url,
            },
            'fields': fields,
        }
        return parsed_embed

    def send_to_discord(self, channel_id: int, embed: Embed):
        url = f'https://discordapp.com/api/v8/channels/{channel_id}/messages'
        payload = {
            'embeds': [self.to_dict(embed)],
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bot {self.discord_token}',
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response
