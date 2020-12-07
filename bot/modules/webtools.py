"""Bot development modules."""

import codecs
import platform
from datetime import datetime
from platform import python_version
import aiohttp
from psutil import boot_time, cpu_percent, disk_usage, virtual_memory
from pytz import timezone

from discord import Embed, __version__
from discord.ext import commands

from bot import bot
from bot.utils import send_typing


@bot.command()
@send_typing
async def invite(ctx):
    """Send an invite link of this bot."""
    embed = Embed(
        color=0xFFB6C1,
        description=(
            "[Here My invite link]"
            "(https://discord.com/oauth2/authorize?"
            "client_id=775903023821881374&permissions=522304&scope=bot)"
            ),
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
        "[Here](https://github.com/keselekpermen69/MyClassScrape) My source code.\n"
        f"You can contact [my owner](https://discord.com/users/{owner.id}) if you wan't to Help :)")
    embed = Embed(color=0xFFB6C1, description=text)
    embed.set_footer(text=owner, icon_url=icon)
    await ctx.send(embed=embed)


@bot.command()
@send_typing
async def sysinfo(ctx):
    """Send bot system information."""
    uptime = datetime.fromtimestamp(boot_time()).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    status = "**========[ SYSTEM INFO ]========**\n"
    status += "**System uptime:** " + str(uptime) + "\n"

    uname = platform.uname()
    status += "**System:** " + str(uname.system) + "\n"
    status += "**Node name:** " + str(uname.node) + "\n"
    status += "**Release:** " + str(uname.release) + "\n"
    status += "**Version:** " + str(uname.version) + "\n"
    status += "**Machine:** " + str(uname.machine) + "\n"
    status += "**Processor:** " + str(uname.processor) + "\n\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += "**CPU usage:** " + str(cpu) + " %\n"
    status += "**Ram usage:** " + str(mem[2]) + " %\n"
    status += "**Storage used:** " + str(disk[3]) + " %\n\n"
    status += "**Python version:** " + python_version() + "\n"
    status += "**Discord.py version:** " + str(__version__) + ""

    embed = Embed(
        color=0xF494ce, description=status
    )
    await ctx.send(embed=embed)


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
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://nekobin.com/api/documents",
            json={"content": data}
        ) as res:
            if res.status != 200:
                response = await res.json()
                key = response['result']['key']
                url = f"https://nekobin.com/raw/{key}"
            else:
                return await ctx.send("Fail to reach nekobin.")
    timenow = datetime.now(timezone("Asia/Jakarta"))
    embed = Embed(
        color=0xFF0000, description=f"Bot log [here]({url})", timestamp=timenow
    )
    await ctx.send(embed=embed)
