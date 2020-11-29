import discord

from importlib import import_module

from bot import bot, BOT_TOKEN, BOT_PREFIX, LOGGER
from bot.modules import ALL_MODULES
from bot.utils import send_typing

HELP_STRING = f"""
my prefix is `{BOT_PREFIX}`

Below you can see all the commands I know.

`help    `= Display this help menu.
`getclass`= Get your class schedule `alias[myclass, schedule]`.
`invite  `= Get my invite link.
`auth    `= Save your credentials `alias[save]`
`ping    `= Check my latency to Discord WebSocket.
`source  `= link to my source code `alias[src]`.
"""


for module in ALL_MODULES:
    imported_module = import_module("bot.modules." + module)


@bot.event
async def on_ready():
    activity = discord.Activity(
        name=f"BinusMaya | {BOT_PREFIX}help",
        type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.command()
@send_typing
async def help(ctx):
    app = await bot.application_info()
    owner = app.owner
    icon = owner.avatar_url_as(static_format="png")
    embed = discord.Embed(
        color=0x9b59b6,
        title="**Hello there!**",
        description=HELP_STRING)
    embed.set_footer(text=f"Made with 💖 by {owner}", icon_url=icon)
    await ctx.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(
        color=0x9b59b6,
        title="**Hello there!**",
        description=f"Thank you For inviting me \
                            \nYou can type `{BOT_PREFIX}help` to see my commands")
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=embed)
            break
    app = await bot.application_info()
    owner = app.owner
    await owner.send(f"Bot joined to **{guild.name}**")


if __name__ == "__main__":
    LOGGER.info("Modules Loaded: " + str(ALL_MODULES))
    bot.run(BOT_TOKEN)
