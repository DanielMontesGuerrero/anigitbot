import re
from hikari.embeds import Embed
import lightbulb

from utils import get_prs_embed, get_pr_embed

plugin = lightbulb.Plugin('pull_requests')

@plugin.command()
@lightbulb.option('index', 'index of pr to query', default='all')
@lightbulb.option('state', 'state of pr\'s to query (all, open, closed)', default='open')
@lightbulb.option('repo', 'name of the repository')
@lightbulb.option('user', 'User owner of the repo')
@lightbulb.command('pr', 'Returns pull requests of given repository')
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def show_pull_requests(ctx: lightbulb.Context) -> None:
    try:
        pull_requests = ctx.app.github.get_pull_requests(ctx.options.user, ctx.options.repo, ctx.options.state)
        embed = Embed()
        if re.match(r'^\d+$', ctx.options.index):
            for index, pr in enumerate(pull_requests):
                if index == int(ctx.options.index) - 1:
                    embed = get_pr_embed(pr)
                    break
        else:
            embed = get_prs_embed(pull_requests, ctx.options.repo)
        await ctx.respond(embed)
    except Exception as error:
        print(error)
        await ctx.respond('Error handling command: ', error)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
