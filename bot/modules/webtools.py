"""Bot development modules."""

import codecs
import platform
import sys
from datetime import datetime

import aiohttp
import psutil
from aiohttp.client_exceptions import ClientConnectionError
from discord import Embed, __version__
from discord.ext import commands
from pytz import timezone

from bot import bot
from bot.utils import send_typing


@bot.command()
@send_typing
async def invite(ctx):
    """Send an invite link of this bot."""
    embed = Embed(
        color=0xFFB6C1,
        description=("http://mrmiss.me/MyClassScrape"),
    )
    await ctx.send(embed=embed)


@bot.command()
@send_typing
async def ping(ctx):
    """Get bot latency from discord websocket."""
    latency = bot.latency
    await ctx.send("Pong! {:.2f}ms".format(latency * 1000))


@bot.command(aliases=["src"])
@send_typing
async def source(ctx):
    """Send source repo of this bot."""
    app = await bot.application_info()
    owner = app.owner
    icon = owner.avatar_url_as(static_format="png")
    text = (
        "[Here](https://github.com/keselekpermen69/MyClassScrape) my source code.\n"
        "and you might want to see my [Unofficial REST API](https://github.com/MrMissx/Binus_API)\n"
        "Feel free to contribute there :)")
    embed = Embed(color=0xFFB6C1, description=text)
    embed.set_footer(text=f"by {owner}", icon_url=icon)
    await ctx.send(embed=embed)


@bot.command()
@send_typing
async def sysinfo(ctx):
    """Send bot system information."""
    uptime = datetime.fromtimestamp(psutil.boot_time()).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    status = "**System uptime : ** " + str(uptime) + "\n"

    uname = platform.uname()
    # System Info
    status += "**System : ** " + str(uname.system) + "\n"
    status += "**Kernel : ** " + str(uname.release) + "\n"
    status += "**Version : ** " + str(uname.version) + "\n"
    status += "**Machine : ** " + str(uname.machine) + "\n"
    status += "**Processor : ** " + str(uname.processor) + "\n\n"

    # CPU info
    status += "**CPU Info**\n"
    status += "**Physical cores : **" + str(psutil.cpu_count(logical=False))+ "\n"
    status += "**Total cores : **" + str(psutil.cpu_count(logical=True))+ "\n"
    status += "**Total cores : **" + str(psutil.cpu_count(logical=True))+ "\n"
    status += "**CPU Usage:**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        status += f"**× Core {i}  **: {percentage}%\n"
    status += "**Total Usage : **" + str(psutil.cpu_percent())+"%\n\n"

    # Memory info
    svmem = psutil.virtual_memory()
    status += "**Memory Info**\n"
    status += "**Total : **" + str(await get_size(svmem.total)) +"\n"
    status += f"**Used : ** {str(await get_size(svmem.used))} ({svmem.percent}%)\n"
    status += "**Available : **" + str(await get_size(svmem.available)) + "\n\n"

    # Bandwith info
    status += "**Bandwith Info**\n"
    status += "**Upload : **" + str(await get_size(psutil.net_io_counters().bytes_sent)) +"\n"
    status += "**Download : **" + str(await get_size(psutil.net_io_counters().bytes_recv)) +"\n"
    status += "**Storage used:** " + str(psutil.disk_usage("/")[3]) + " %\n\n"

    status += "**Lib version**\n"
    status += "**Python version:** " + str(sys.version) + "\n"
    status += "**Discord.py version:** " + str(__version__)

    embed = Embed(
        color=0xF494ce, description=status, title="**SYSTEM INFO**",
    )
    await ctx.send(embed=embed)


async def get_size(byte, suffix="B"):
    """Get human readable format."""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if byte < factor:
            return f"{byte:.2f}{unit}{suffix}"
        byte /= factor


@commands.is_owner()
@bot.command(aliases=["log"])
@send_typing
async def logs(ctx):
    """
    Send a all logs as file.
    (only owner can trigger this).
    """
    with codecs.open("ClassScraper.log", "r", encoding="utf-8") as log_file:
        data = log_file.read()
    link = await push_hastebin(data)
    if not link:
        return await ctx.send("Fail to reach hastebin.")
    timenow = datetime.now(timezone("Asia/Jakarta"))
    embed = Embed(
        color=0xFF0000, description=f"Bot log [here]({link})", timestamp=timenow
    )
    await ctx.send(embed=embed)


async def push_hastebin(data) -> str:
    """Upload a text to pastebin"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "https://hastebin.com/documents",
                data=data.encode("utf-8"),
            ) as res:
                if res.status == 200:
                    response = await res.json()
                    return f"https://hastebin.com/{response['key']}"
                else:
                    return False
        except ClientConnectionError:
            return False
