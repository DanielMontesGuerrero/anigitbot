import lightbulb

from src.db.db import session as db_session
from src.db.models import NotifyList


plugin = lightbulb.Plugin('notifications')

@plugin.command()
@lightbulb.command('notifyme', 'Subscribe to notifications')
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def notifyme(ctx: lightbulb.Context) -> None:
    mentions = db_session.query(NotifyList).filter_by(
        discord_username=ctx.author.username,
    ).all()
    message = ('You will recieve notifications for the following github users:\n'
               + '\n'.join([user.github_username for user in mentions])
               + '\nUse add/remove to change your subscriptions.')
    await ctx.respond(message)

@notifyme.child
@lightbulb.option('git_user', 'Github username')
@lightbulb.command('add', 'Add notifications for github user')
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def add(ctx: lightbulb.Context) -> None:
    discord_user = ctx.author.username
    notify = NotifyList(discord_user, ctx.options.git_user, ctx.author.mention)
    db_session.add(notify)
    db_session.commit()
    await ctx.respond(
        f'{ctx.author.mention} will be notified in github @{ctx.options.git_user} mentions',
    )

@notifyme.child
@lightbulb.option('git_user', 'Github username')
@lightbulb.command('remove', 'Remove notifications of github user')
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def remove(ctx: lightbulb.Context) -> None:
    db_session.query(NotifyList).filter_by(
        discord_username=ctx.author.username,
        github_username=ctx.options.git_user,
    ).delete()
    await ctx.respond(
        f'{ctx.author.mention} will NOT be notified in github '
        + f'@{ctx.options.git_user} mentions anymore',
    )

@notifyme.child
@lightbulb.command('list', 'List my subscriptions')
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def list(ctx: lightbulb.Context) -> None:
    mentions = db_session.query(NotifyList).filter_by(
        discord_username=ctx.author.username,
    ).all()
    message = ('You will recieve notifications for the following github users:\n'
               + '\n'.join([user.github_username for user in mentions])
               + '\nUse add/remove to change your subscriptions.')
    await ctx.respond(message)

async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    await event.context.respond('Error handling command :(, check params and try again')

plugin.set_error_handler(on_error)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
