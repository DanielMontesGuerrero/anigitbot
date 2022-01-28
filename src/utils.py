from typing import List, Union
from github3.issues.issue import Issue
from github3.pulls import PullRequest
from github3.structs import GitHubIterator
from hikari.colors import Color
from hikari.embeds import Embed
from src.waifu import get_random_waifu
from src.db.db import session as db_session
from src.db.models import NotifyChannelList, NotifyUserList


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
            value=f'Owner: {pr.user.login}\nState: {pr.state}\nLink: {pr.html_url}',
        )
    return embed

def get_pr_embed(pr: PullRequest) -> Embed:
    embed = Embed(
        title=f'{pr.title}',
        description=pr.body_text,
        color=get_color_from_state(pr.state),
        url=pr.html_url,
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

def get_issues_embed(issues: GitHubIterator, repository_name: str) -> Embed:
    embed = Embed(
        title=f'Issues of {repository_name}',
        color=Color.of('#F09C35'),
    )
    waifu_url = get_random_waifu()
    embed.set_thumbnail(waifu_url)
    waifu_url = get_random_waifu()
    embed.set_image(waifu_url)
    for index, issue in enumerate(issues):
        embed.add_field(
            name=f'{index + 1}. {issue.title}',
            value=f'Owner: {issue.user.login}\nState: {issue.state}\nLink: {issue.html_url}',
        )
    return embed

def get_issue_embed(issue: Issue) -> Embed:
    embed = Embed(
        title=f'{issue.title}',
        description=issue.body_text,
        color=get_color_from_state(issue.state),
        url=issue.html_url,
    )
    embed.set_thumbnail(issue.user.avatar_url)
    embed.add_field(name='Author', value=issue.user.login)
    embed.add_field(name='State', value=issue.state)
    reviewers = [user.login for user in issue.assignees]
    reviewers_str = '\n'.join(reviewers)
    if reviewers_str != '':
        embed.add_field(name='Assignees', value=reviewers_str)
    waifu_url = get_random_waifu()
    embed.set_image(waifu_url)
    return embed

def get_color_from_state(state: str) -> Color:
    if state == 'open':
        return Color.of('#42f545')
    else:
        return Color.of('#f54242')

def get_mentions_from(obj: Union[PullRequest, Issue]) -> List[str]:
    users = []
    if isinstance(obj, PullRequest):
        users = obj.requested_reviewers
    else:
        users = obj.assignees
    reviewers = [user.login for user in users]
    mentions = db_session.query(NotifyUserList).filter(
        NotifyUserList.github_username.in_(reviewers),
    )
    return [user.mention for user in mentions]

def get_channel_list(user: str, repo: str) -> List[int]:
    notify_list = db_session.query(NotifyChannelList).filter_by(
        github_username=user,
        github_repo=repo,
    ).all()
    return [notify.discord_channel for notify in notify_list]
