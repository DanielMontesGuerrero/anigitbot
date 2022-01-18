import lightbulb
import re

from hikari.embeds import Embed
from src.utils import get_mentions_from, get_issues_embed, get_issue_embed


plugin = lightbulb.Plugin('issues')

@plugin.command()
@lightbulb.option('index', 'index of pr to query', default='all')
@lightbulb.option('state', 'state of issues to query (all, open, closed)', default='open')
@lightbulb.option('repo', 'name of the repository')
@lightbulb.option('user', 'User owner of the repo')
@lightbulb.command('issue', 'Returns issues of given repository')
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def issue(ctx: lightbulb.Context) -> None:
    issues = ctx.app.github.get_issues(
        ctx.options.user,
        ctx.options.repo,
        ctx.options.state,
    )
    embed = Embed()
    mentions = set()
    if re.match(r'^\d+$', ctx.options.index):
        for index, _issue in enumerate(issues):
            if index == int(ctx.options.index) - 1:
                embed = get_issue_embed(_issue)
                mentions = get_mentions_from(_issue)
                break
    else:
        for _issue in issues:
            mentions.update(get_mentions_from(_issue))
        embed = get_issues_embed(issues, ctx.options.repo)
    mentions_str = ' '.join(mentions)
    if mentions_str != '':
        await ctx.respond(mentions_str)
    await ctx.respond(embed)

async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    await event.context.respond('Error handling command :(, check params and try again')

plugin.set_error_handler(on_error)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
