import re
import lightbulb

from hikari.embeds import Embed
from src.utils import get_mentions_from_pr, get_prs_embed, get_pr_embed


plugin = lightbulb.Plugin('pull_requests')

@plugin.command()
@lightbulb.option('index', 'index of pr to query', default='all')
@lightbulb.option('state', 'state of pr\'s to query (all, open, closed)', default='open')
@lightbulb.option('repo', 'name of the repository')
@lightbulb.option('user', 'User owner of the repo')
@lightbulb.command('pr', 'Returns pull requests of given repository')
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def show_pull_requests(ctx: lightbulb.Context) -> None:
    pull_requests = ctx.app.github.get_pull_requests(
        ctx.options.user,
        ctx.options.repo,
        ctx.options.state,
    )
    embed = Embed()
    mentions = set()
    if re.match(r'^\d+$', ctx.options.index):
        for index, pr in enumerate(pull_requests):
            if index == int(ctx.options.index) - 1:
                embed = get_pr_embed(pr)
                mentions = get_mentions_from_pr(pr)
                break
    else:
        for pr in pull_requests:
            mentions.update(get_mentions_from_pr(pr))
        embed = get_prs_embed(pull_requests, ctx.options.repo)
    mentions_str = ' '.join(mentions)
    if mentions_str != '':
        await ctx.respond(mentions_str)
    await ctx.respond(embed)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
