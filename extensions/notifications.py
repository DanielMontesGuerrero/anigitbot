from github3 import github
import lightbulb

from src.db.db import session as db_session
from src.db.models import NotifyChannelList, NotifyUserList


plugin = lightbulb.Plugin('notifications')

@plugin.command()
@lightbulb.command('notifyme', 'Subscribe to notifications')
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def notifyme(ctx: lightbulb.Context) -> None:
    mentions = db_session.query(NotifyUserList).filter_by(
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
    notify = NotifyUserList(discord_user, ctx.options.git_user, ctx.author.mention)
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
    db_session.query(NotifyUserList).filter_by(
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
    mentions = db_session.query(NotifyUserList).filter_by(
        discord_username=ctx.author.username,
    ).all()
    message = ('You will recieve notifications for the following github users:\n'
               + '\n'.join([user.github_username for user in mentions])
               + '\nUse add/remove to change your subscriptions.')
    await ctx.respond(message)

@plugin.command()
@lightbulb.command('notifyc', 'Subscribe this channel to notifications')
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def notifyc(ctx: lightbulb.Context) -> None:
    mentions = db_session.query(NotifyChannelList).filter_by(
        discord_channel=ctx.channel_id,
    ).all()
    message = ('This channel will recieve notifications for the following github repos:\n'
               + '\n'.join([
                   f'{notify.github_username}/{notify.github_repo}' for notify in mentions
               ])
               + '\nUse add/remove to change the subscriptions.')
    await ctx.respond(message)

@notifyc.child
@lightbulb.option('git_repo', 'Github repo')
@lightbulb.option('git_user', 'Github username')
@lightbulb.command('add', 'Add notifications for github repo')
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def notifyc_add(ctx: lightbulb.Context) -> None:
    channel_id = ctx.channel_id
    notify = NotifyChannelList(channel_id, ctx.options.git_user, ctx.options.git_repo)
    db_session.add(notify)
    db_session.commit()
    await ctx.respond(
        'This channel will be notified in github repo '
        + f'{ctx.options.git_user}/{ctx.options.git_repo} events',
    )

@notifyc.child
@lightbulb.option('git_repo', 'Github repo')
@lightbulb.option('git_user', 'Github username')
@lightbulb.command('remove', 'Remove notifications of github repo')
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def notifyc_remove(ctx: lightbulb.Context) -> None:
    db_session.query(NotifyChannelList).filter_by(
        discord_channel=ctx.channel_id,
        github_username=ctx.options.git_user,
        github_repo=ctx.options.git_repo,
    ).delete()
    await ctx.respond(
        f'This channel will NOT be notified in github '
        + f'{ctx.options.git_user}/{ctx.options.git_repo} events anymore',
    )

@notifyc.child
@lightbulb.command('list', 'List subscriptions of channel')
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def notifyc_list(ctx: lightbulb.Context) -> None:
    mentions = db_session.query(NotifyChannelList).filter_by(
        discord_channel=ctx.channel_id,
    ).all()
    message = ('This channel will recieve notifications for the following github repos:\n'
               + '\n'.join([
                   f'{notify.github_username}/{notify.github_repo}' for notify in mentions
               ])
               + '\nUse add/remove to change the subscriptions.')
    await ctx.respond(message)

async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    await event.context.respond('Error handling command :(, check params and try again')

plugin.set_error_handler(on_error)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
