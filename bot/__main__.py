import asyncio
import discord

from datetime import datetime, time, timedelta
from importlib import import_module

from bot import (
    bot,
    BOT_TOKEN,
    BOT_PREFIX,
    SCHEDULE_CHANNEL,
    TASK_MSG_PLACEHOLDER,
    DAILY_TASK,
    LOGGER
    )
from bot.modules import ALL_MODULES
from bot.modules.scraper import getclass

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

DailyTask_time = time(hour=23)  # 11PM UTC

for module in ALL_MODULES:
    imported_module = import_module("bot.modules." + module)


@bot.command()
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


async def startup():
    await bot.wait_until_ready()
    LOGGER.info("Setting up Bot status")
    activity = discord.Activity(
        name=f"BinusMaya | {BOT_PREFIX}help",
        type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    if DAILY_TASK:
        # Bot task to run daily
        LOGGER.info("Running DAILY_TASK every {} UTC".format(DailyTask_time))
        task = asyncio.create_task(DailyTask())
        task.add_done_callback(task_exeption)

    LOGGER.info("Bot started")


async def _create_context(channel, message_id):
    """Create a ctx from a channel message placeholder"""
    channel = bot.get_channel(channel)
    message = await channel.fetch_message(id=message_id)
    return await bot.get_context(message)


async def _schedule(ctx):
    await getclass(ctx, args="now", is_scheduler=True)
    LOGGER.info("Daily task complete")


async def DailyTask():
    """Create a daily task."""
    while True:
        now = datetime.utcnow()
        date = now.date()
        if now.time() > DailyTask_time:
            date = now.date() + timedelta(days=1)
        then = datetime.combine(date, DailyTask_time)
        await discord.utils.sleep_until(then)
        LOGGER.info("Running daily schedule task")
        ctx = await _create_context(SCHEDULE_CHANNEL, TASK_MSG_PLACEHOLDER)
        await _schedule(ctx)


def task_exeption(task):
    """Handle exception on scheduler task"""
    if task.exception():
        task.print_stack()


if __name__ == "__main__":
    LOGGER.info("Modules Loaded: " + str(ALL_MODULES))
    bot.loop.create_task(startup())
    bot.run(BOT_TOKEN)
