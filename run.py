import sys
import os

from anigitbot import Anigitbot
from src.db import db
from src.db.models import NotifyUserList, NotifyChannelList


def run():
    if len(sys.argv) > 1:
        discord_token = sys.argv[1]
    else:
        discord_token = os.getenv('DISCORD_TOKEN')
    if len(sys.argv) > 2:
        github_token = sys.argv[2]
    else:
        github_token = os.getenv('GITHUB_TOKEN')

    bot = Anigitbot(discord_token=discord_token, github_token=github_token)

    bot.load_extensions_from('./extensions')
    bot.run()

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    run()
