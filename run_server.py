import sys

from http.server import HTTPServer
from http_handler import Handler
from functools import partial
from anigitbot import Anigitbot


def run():
    discord_token = sys.argv[1]
    github_token = sys.argv[2]
    port = int(sys.argv[3])
    handler = partial(Handler, discord_token, github_token)
    with HTTPServer(('', port), handler) as server:
        server.serve_forever()

if __name__ == '__main__':
    run()
