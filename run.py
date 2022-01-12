import sys

from anigitbot import Anigitbot

def run():
    discord_token = sys.argv[1]
    github_token = sys.argv[2]

    bot = Anigitbot(discord_token=discord_token, github_token=github_token)

    bot.load_extensions_from('./extensions')
    bot.run()

if __name__ == '__main__':
    run()
