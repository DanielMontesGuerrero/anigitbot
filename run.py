from anigitbot import Anigitbot

def run():
    discord_token = 'OTI5MTQ2NzAxMjEyNzA0ODQx.YdjFTA._WijXua8MXDj-RZTyZgAteuoaOY'
    github_token = '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'

    # bot = lightbulb.BotApp(token=discord_token)
    bot = Anigitbot(discord_token=discord_token, github_token=github_token)

    bot.load_extensions_from('./extensions')
    bot.run()

if __name__ == '__main__':
    run()
