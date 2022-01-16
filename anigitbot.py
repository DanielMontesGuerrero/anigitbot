import lightbulb

from src.github_handler import GithubHandler


class Anigitbot(lightbulb.BotApp):
    def __init__(self,  *args, **kwargs):
        if 'github_token' not in kwargs:
            raise   Exception('Missing github token')
        if 'discord_token' not in kwargs:
            raise   Exception('Missing discord token')
        super().__init__(token=kwargs['discord_token'], prefix='!')
        self.github = GithubHandler(kwargs['github_token'])

