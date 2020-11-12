import discord

from bot import bot, BOT_PREFIX, LOGGER
import bot.modules.sql.cred_sql as credata
from bot.utils import encrypt, decrypt


@bot.command(aliases=['save'])
async def auth(ctx, cred: str=None):
    author = ctx.author

    if cred == None:  # if no credential given
        text = f"`{BOT_PREFIX}auth <username>$<password>`\
                \n\n*username without @binus.ac.id"
        embed = discord.Embed(color=0x9b59b6, description=text, title="**Please enter your credential with this format**")
        await author.send(embed=embed)
        if ctx.guild is not None:  # dont send if in PM's
            await ctx.send("I've send the help on PM's :)")
        return

    try:
        uname, sec = cred.split("$")
    except ValueError:
        ctx.send("Please send your credential like the format given")
        return
    a = credata.save_cred(author.id, encrypt(uname), encrypt(sec))
    if a:
        await ctx.send("Credentials saved successfully")
        return
    else:  # sad life
        user = author.name + "#" + author.discriminator
        await ctx.send("Seems something broke...\nwould you mind to tell my owner :)")
        LOGGER.error(f"Error saving cred from {user}")
        return
