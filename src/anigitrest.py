import hikari

from src.github_handler import GithubHandler
from src.utils import get_pr_embed

class Anigitrest(hikari.RESTApp):
    def __init__(self,  *args, **kwargs):
        if 'github_token' not in kwargs:
            raise   Exception('Missing github token')
        if 'discord_token' not in kwargs:
            raise   Exception('Missing discord token')
        super().__init__()
        self.github = GithubHandler(kwargs['github_token'])
        self.discord_token = kwargs['discord_token']

    async def notify_pull_request(self, channel_id: int, user: str, repository_name: str, pr_number: int) -> None:
        async with self.acquire(self.discord_token, token_type='Bot') as client:
            pr = self.github.get_pull_request(user, repository_name, pr_number)
            embed = get_pr_embed(pr)
            await client.create_message(
                channel=channel_id,
                embed=embed,
                content='@everyone',
            )
