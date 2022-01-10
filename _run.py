import logging
from gitbot import Gitbot

logging.basicConfig(level=logging.INFO)

discord_token = 'OTI5MTQ2NzAxMjEyNzA0ODQx.YdjFTA.D5dxnDx645d4C3axCgDKlFzJjjY'
github_token = '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'

client = Gitbot(github_token=github_token)

client.run(discord_token)
