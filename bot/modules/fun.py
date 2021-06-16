import aiohttp

from discord import Embed

from bot import bot
from bot.utils import check_nsfw

base_neko_url = "https://www.nekos.life/api/v2/img/"


@bot.command()
async def avatar(ctx):
    if ctx.message.mentions:
        user = ctx.message.mentions[0]  # only get the first user
    else:
        user = ctx.author
    url = user.avatar_url
    embed = Embed(
        color=0xF5ABC9,
        title=f"{user.name}#{user.discriminator}",
        url=url
    )
    embed.set_image(url=url)
    await ctx.send(embed=embed)


@bot.command(aliases=["nyan"])
async def neko(ctx):
    url = await request("neko")
    await ctx.send(embed=build_embed("Neko", url))


@bot.command()
async def slap(ctx):
    url = await request("slap")
    await ctx.send(embed=build_embed("Slaps", url))


@bot.command()
async def baka(ctx):
    url = await request("baka")
    await ctx.send(embed=build_embed("Baka", url))


@bot.command()
async def kiss(ctx):
    url = await request("kiss")
    await ctx.send(embed=build_embed("Kiss", url))


@bot.command(aliases=["wallpaper", "wp"])
async def wall(ctx):
    url = await request("wallpaper")
    await ctx.send(embed=build_embed("Wallpaper", url))


@bot.command(aliases=["kitsune"])
async def fox_girl(ctx):
    url = await request("fox_girl")
    await ctx.send(embed=build_embed("Kitsune", url))


@bot.command(aliases=["hentai"])
@check_nsfw
async def hent(ctx):
    url = await request("hentai")
    await ctx.send(embed=build_embed("Hentai", url))


@bot.command(aliases=["pussy"])
@check_nsfw
async def pus(ctx):
    url = await request("pussy")
    await ctx.send(embed=build_embed("Pussy", url))


@bot.command(aliases=["yuri"])
@check_nsfw
async def yr(ctx):
    url = await request("yuri")
    await ctx.send(embed=build_embed("Yuri", url))


async def request(img_type: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(base_neko_url + img_type) as res:
            url = await res.json()
    return url.get("url", None)


def build_embed(title: str, url: str) -> Embed:
    embed = Embed(color=0xFFB6C1, title=title, url=url)
    embed.set_image(url=url)
    embed.set_footer(text="Powered by nekos.life")
    return embed
