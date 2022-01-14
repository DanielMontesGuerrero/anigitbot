from http.server import BaseHTTPRequestHandler
import urllib.parse
import asyncio
from anigitbot import Anigitrest

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
        anigitrest = Anigitrest(discord_token=self.discord_token, github_token=self.github_token)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(anigitrest.notify_pull_request(channel_id, user, repository_name, pr_number))
