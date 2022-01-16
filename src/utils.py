from github3.pulls import PullRequest
from github3.structs import GitHubIterator
from hikari.colors import Color
from hikari.embeds import Embed
from src.waifu import get_random_waifu


def get_prs_embed(pull_requests: GitHubIterator, repository_name: str) -> Embed:
    embed = Embed(
        title=f'Pull requests of {repository_name}',
        color=Color.of('#3440eb'),
    )
    waifu_url = get_random_waifu()
    embed.set_thumbnail(waifu_url)
    waifu_url = get_random_waifu()
    embed.set_image(waifu_url)
    for index, pr in enumerate(pull_requests):
        embed.add_field(
            name=f'{index + 1}. {pr.title}',
            value=f'Owner: {pr.user.login}\nState: {pr.state}\nLink: {pr.url}',
        )
    return embed

def get_pr_embed(pr: PullRequest) -> Embed:
    embed = Embed(
        title=f'{pr.title}',
        description=pr.body,
        color=get_color_from_state(pr.state),
        url=pr.url,
    )
    embed.set_thumbnail(pr.user.avatar_url)
    embed.add_field(name='Author', value=pr.user.login)
    embed.add_field(name='State', value=pr.state)
    reviewers = [user.login for user in pr.requested_reviewers]
    reviewers_str = '\n'.join(reviewers)
    if reviewers_str != '':
        embed.add_field(name='Reviewers', value=reviewers_str)
    waifu_url = get_random_waifu()
    embed.set_image(waifu_url)
    return embed

def get_color_from_state(state: str) -> Color:
    if state == 'open':
        return Color.of('#42f545')
    else:
        return Color.of('#f54242')
