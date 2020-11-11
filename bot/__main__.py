import discord

from importlib import import_module
from bot.modules import ALL_MODULES
from bot import bot, BOT_TOKEN, BOT_PREFIX, LOGGER, OWNER_ID


HELP_STRING=f"""
**Hello there!**
my prefix is `{BOT_PREFIX}`

Below you can see all the commands I know.
`help    `= Display this help menu.
`getclass`= Get your class schedule from.
`invite  `= Get my invite link.
`ping    `=
`source  `= link to my source code `alias[src]`.

"Made by 💖 [Mr.Miss](https://discord.com/users/{OWNER_ID})"
"""


for module in ALL_MODULES:
    imported_module = import_module("bot.modules." + module)

@bot.event
async def on_ready():
    activity = discord.Activity(name=f"BinusMaya | {BOT_PREFIX}help", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.command()
async def help(ctx):
    embed = discord.Embed(color=0x9b59b6, description=HELP_STRING)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
