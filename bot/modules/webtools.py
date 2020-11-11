from bot import bot, OWNER_ID
from datetime import datetime
from discord import Embed


@bot.command()
async def invite(ctx):
    embed = Embed(color=0xffb6c1,
        description="[Here My invite link](https://discord.com/api/oauth2/authorize?client_id=775903023821881374&permissions=8&scope=bot)")
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send("Pong! {:.2f}ms".format(latency*1000))


@bot.command(aliases=['src'])
async def source(ctx):
    text = "My source code is curently in private since this bot still in development.\n"
    text += f"You can contact [my owner](https://discord.com/users/{OWNER_ID}) if you wan't to support :)"
    embed = Embed(color=0xffb6c1, description=text)
    await ctx.send(embed=embed)
