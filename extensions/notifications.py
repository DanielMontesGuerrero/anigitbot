import lightbulb


plugin = lightbulb.Plugin('notifications')

@plugin.command()
@lightbulb.command('notifyme', 'Subscribe to notifications')
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def subscribe(ctx: lightbulb.Context) -> None:
    await ctx.respond(f'{ctx.author.mention} will be notified')

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
