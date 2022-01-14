import sys
import os

from http.server import HTTPServer
from http_handler import Handler
from functools import partial
from anigitbot import Anigitbot


def run():
    if len(sys.argv) > 1:
        discord_token = sys.argv[1]
    else:
        discord_token = os.getenv('DISCORD_TOKEN')
    if len(sys.argv) > 2:
        github_token = sys.argv[2]
    else:
        github_token = os.getenv('GITHUB_TOKEN')
    if len(sys.argv) > 3:
        port = int(sys.argv[3])
    else:
        port = int(os.getenv('PORT'))
    handler = partial(Handler, discord_token, github_token)
    with HTTPServer(('', port), handler) as server:
        server.serve_forever()

if __name__ == '__main__':
    run()
