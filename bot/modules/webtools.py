from bot import bot, OWNER_ID
from datetime import datetime
from discord import Embed


@bot.command()
async def invite(ctx):
    embed = Embed(color=0xffb6c1,
        description="[Here My invite link](https://discord.com/oauth2/authorize?client_id=775903023821881374&permissions=522304&scope=bot)")
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send("Pong! {:.2f}ms".format(latency*1000))


@bot.command(aliases=['src'])
async def source(ctx):
    icon = "https://cdn.discordapp.com/avatars/302015492154195968/00d7e6ee6aef91a302f89ce10c3089f8.png?size=1024"
    text = ("[Here](https://github.com/keselekpermen69/MyClassScrape) My source code.\n"
            f"You can contact [my owner](https://discord.com/users/{OWNER_ID}) if you wan't to support :)"
    )

    embed = Embed(color=0xffb6c1, description=text)
    embed.set_footer(text="Mr.Miss#6333", icon_url=icon)
    await ctx.send(embed=embed)
