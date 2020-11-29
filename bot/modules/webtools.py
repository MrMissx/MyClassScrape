import codecs
import heroku3
import os
import requests

from bot import bot, HEROKU_APP_NAME, HEROKU_API_KEY, LOGGER
from bot.utils import send_typing

from datetime import datetime
from discord import Embed
from discord.ext import commands
from pytz import timezone


@bot.command()
@send_typing
async def invite(ctx):
    embed = Embed(
        color=0xffb6c1,
        description="[Here My invite link](https://discord.com/oauth2/authorize?client_id=775903023821881374&permissions=522304&scope=bot)")
    await ctx.send(embed=embed)


@bot.command()
@send_typing
async def ping(ctx):
    latency = bot.latency
    await ctx.send("Pong! {:.2f}ms".format(latency * 1000))


@bot.command(aliases=['src'])
@send_typing
async def source(ctx):
    app = await bot.application_info()
    owner = app.owner
    icon = owner.avatar_url_as(static_format="png")
    text = (
        "[Here](https://github.com/keselekpermen69/MyClassScrape) My source code.\n"
        f"You can contact [my owner](https://discord.com/users/{owner.id}) if you wan't to Help :)")
    embed = Embed(color=0xffb6c1, description=text)
    embed.set_footer(text=owner, icon_url=icon)
    await ctx.send(embed=embed)


@commands.is_owner()
@bot.command(aliases=['log'])
@send_typing
async def logs(ctx):
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        LOGGER.error("NO HEROKU_API_KEY or HEROKU_APP_NAME")
        return
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    fd = codecs.open("logs.txt", "r", encoding="utf-8")
    data = fd.read()
    key = (requests.post("https://nekobin.com/api/documents",
                            json={"content": data}) .json() .get("result") .get("key"))
    url = f"https://nekobin.com/raw/{key}"
    timenow = datetime.now(timezone("Asia/Jakarta"))
    embed = Embed(
        color=0xff0000,
        description=f"Bot log [here]({url})",
        timestamp=timenow)
    await ctx.send(embed=embed)
    return os.remove("logs.txt")
