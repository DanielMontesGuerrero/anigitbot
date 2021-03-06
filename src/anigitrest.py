import hikari

from src.github_handler import GithubHandler
from src.utils import get_channel_list, get_mentions_from, get_pr_embed, get_issue_embed


class Anigitrest(hikari.RESTApp):
    def __init__(self,  *args, **kwargs):
        if 'github_token' not in kwargs:
            raise   Exception('Missing github token')
        if 'discord_token' not in kwargs:
            raise   Exception('Missing discord token')
        super().__init__()
        self.github = GithubHandler(kwargs['github_token'])
        self.discord_token = kwargs['discord_token']

    async def notify_pull_request(
        self,
        user: str,
        repository_name: str,
        pr_number: int,
    ) -> None:
        async with self.acquire(self.discord_token, token_type='Bot') as client:
            channels = get_channel_list(user, repository_name)
            pr = self.github.get_pull_request(user, repository_name, pr_number)
            embed = get_pr_embed(pr)
            mentions = get_mentions_from(pr)
            for channel_id in channels:
                await client.create_message(
                    channel=channel_id,
                    embed=embed,
                    content=' '.join(mentions),
                )

    async def notify_issue(
        self,
        user: str,
        repository_name: str,
        issue_number: int,
    ) -> None:
        async with self.acquire(self.discord_token, token_type='Bot') as client:
            channels = get_channel_list(user, repository_name)
            issue = self.github.get_issue(user, repository_name, issue_number)
            embed = get_issue_embed(issue)
            mentions = get_mentions_from(issue)
            for channel_id in channels:
                await client.create_message(
                    channel=channel_id,
                    embed=embed,
                    content=' '.join(mentions),
                )
