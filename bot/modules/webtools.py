"""Bot development modules."""

import codecs
import os
from datetime import datetime
import requests

from discord import Embed
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


@commands.is_owner()
@bot.command(aliases=["log"])
@send_typing
async def logs(ctx):
    """
    Send a all logs as file.
    (only owner can trigger this).
    """
    log_file = codecs.open("ClassScraper.log", "r", encoding="utf-8")
    data = log_file.read()
    key = (requests.post("https://nekobin.com/api/documents",
                         json={"content": data}) .json() .get("result") .get("key"))
    url = f"https://nekobin.com/raw/{key}"
    timenow = datetime.now(timezone("Asia/Jakarta"))
    embed = Embed(
        color=0xFF0000, description=f"Bot log [here]({url})", timestamp=timenow
    )
    await ctx.send(embed=embed)
    return os.remove("logs.txt")
