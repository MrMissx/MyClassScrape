"""Bot startup"""

import asyncio
import traceback
from datetime import datetime, time, timedelta
from importlib import import_module
from pytz import timezone

import discord
from discord.ext.commands import context, errors

from bot import (BOT_PREFIX, BOT_TOKEN, CUSTOM_STATUS, DAILY_TASK,
                 DAILY_TASK_TIME, LOGGER, SCHEDULE_CHANNEL,
                 TASK_MSG_PLACEHOLDER, bot)
from bot.modules import ALL_MODULES
from bot.modules.scraper import getclass

HELP_STRING = f"""
my prefix is `{BOT_PREFIX}`

Below you can see all the commands I know.

`auth    `= Save your credentials `alias[save]`.
`eval    `= Execute a simple **python** scripts `alias[evaluate]`.
`exam    `= Get the latest exam schedule `alias[getexam, myexam]` **__\*Beta__**.
`getclass <args>`= Get your class schedule `alias[myclass, schedule]`.
`help    `= Display this help menu.
`invite  `= Get my invite link.
`ping    `= Check my latency to Discord server.
`source  `= link to my source code `alias[src]`.
`sysinfo `= See my system info i'm running on.
`unauth  `= Delete your saved credentials from my db `alias[gdpr]`.

**Notes:**
You can fetch specific date with getclass command
e.g.: `{BOT_PREFIX}getclass now` -> fetch today's schedule.
avaliable args : today, now, tomorrow\n
You can also use it with numbers (starts from 0)
e.g.: `{BOT_PREFIX}getclass 1`-> fetch tomorrow's schedule.
0 = today; 1 = tomorrow; 2 = day after tomorrow; etc.

You can invite me at [here](http://mrmiss.me/MyClassScrape).
"""

DT_TIME = time(hour=DAILY_TASK_TIME)  # in UTC default -> 23

for module in ALL_MODULES:
    imported_module = import_module("bot.modules." + module)


@bot.command()
async def help(ctx):  # pylint: disable=redefined-builtin
    """Send bot helper."""
    app = await bot.application_info()
    owner = app.owner
    icon = owner.avatar_url_as(static_format="png")
    embed = discord.Embed(
        color=0x9B59B6, title="**Hello there!**", description=HELP_STRING
    )
    embed.set_author(
        name=ctx.me.display_name,
        url="http://mrmiss.me/MyClassScrape",
        icon_url=ctx.me.avatar_url
    )
    embed.set_footer(text=f"Made with 💖 by {owner}", icon_url=icon)
    await ctx.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    """Notify owner for joining guild."""
    embed = discord.Embed(
        color=0x9B59B6,
        title="**Hello there!**",
        description=f"Thank you For inviting me \
                            \nYou can type `{BOT_PREFIX}help` to see my commands",
    )
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=embed)
            break
    app = await bot.application_info()
    owner = app.owner
    await owner.send(f"Bot joined to **{guild.name}**")


@bot.event
async def on_command_error(ctx, error):
    """Send an error message if something wrong."""
    if isinstance(error, errors.CommandNotFound):
        return  # don't flood on unhandled command
    if isinstance(error, errors.NotOwner):
        return await ctx.reply("Only my owner can access this command!", delete_after=5)
    trace = traceback.format_exception(
        type(error), error, error.__traceback__
    )
    err = "".join(trace)
    err_msg = f"{type(error).__name__}({error})"
    message = (
        f"An exception was raised while handling an update [{ctx.command}]\n\n"
        f"{err}"
    )
    embed = discord.Embed(
        color=0xB00020,
        title="An exception was raised while handling an update",
        description=f"```python\n{err_msg}\n```\nThis error has been reported to my owner.",
        timestamp=datetime.now(timezone("Asia/Jakarta"))
    )
    app = await bot.application_info()
    owner = app.owner
    await asyncio.gather(
        ctx.send(embed=embed),
        owner.send(f"```python\n{message}\n```")
    )


async def startup():
    """Task to run when starting up."""
    await bot.wait_until_ready()
    LOGGER.info("Setting up Bot status")
    status = f"BinusMaya | {BOT_PREFIX}help"
    if CUSTOM_STATUS:
        status = CUSTOM_STATUS
    activity = discord.Activity(
        name=status,
        type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    if DAILY_TASK:
        # Bot task to run daily
        LOGGER.info("Running DAILY_TASK every %s UTC", DT_TIME)
        bot.loop.create_task(daily_task())

    # app = await bot.application_info()
    # await app.owner.send("Bot Started!")
    LOGGER.info("Bot started")


async def _create_context(channel, message_id) -> context.Context:
    """Create a ctx from a channel message placeholder"""
    channel = bot.get_channel(channel)
    message = await channel.fetch_message(id=message_id)
    return await bot.get_context(message)


async def _schedule(ctx):
    """Get schedule for daily task."""
    await getclass(ctx, args="now", is_scheduler=True)
    LOGGER.info("Daily task complete")


async def daily_task():
    """Create a daily task."""
    while True:
        now = datetime.utcnow()
        date = now.date()
        if now.time() > DT_TIME:
            date = now.date() + timedelta(days=1)
        then = datetime.combine(date, DT_TIME)
        await discord.utils.sleep_until(then)
        LOGGER.info("Running daily schedule task")
        ctx = await _create_context(SCHEDULE_CHANNEL, TASK_MSG_PLACEHOLDER)
        await _schedule(ctx)


if __name__ == "__main__":
    LOGGER.info("Modules Loaded: %s", str(ALL_MODULES))
    bot.loop.create_task(startup())
    bot.run(BOT_TOKEN)
