import discord

from importlib import import_module
from bot.modules import ALL_MODULES
from bot import bot, BOT_TOKEN, BOT_PREFIX, LOGGER, OWNER_ID


HELP_STRING=f"""
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
    activity = discord.Activity(name=f"BinusMaya | {BOT_PREFIX}help", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.command()
async def help(ctx):
    icon = "https://cdn.discordapp.com/avatars/302015492154195968/00d7e6ee6aef91a302f89ce10c3089f8.png?size=1024"
    embed = discord.Embed(color=0x9b59b6, title="**Hello there!**", description=HELP_STRING)
    embed.set_footer(text="Made with 💖 by Mr.Miss#6333", icon_url=icon)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
