from bot import bot, BOT_PREFIX
import bot.modules.sql.cred_sql as credata
from bot.utils import encrypt, decrypt
from discord import message


@bot.command(aliases=['auth'])
async def save(ctx, cred: str=None):
    if cred == None:
        await ctx.send(f"**Please enter your credential with this format**\
                        \n`{BOT_PREFIX}save <username>$<password>`"
        )
        return

    uname, sec = cred.split("$")
    a = credata.save_cred(ctx.author.id, encrypt(uname), encrypt(sec))
    if a:
        await ctx.send("Credentials saved successfully")
    else:  # sad bug
        await ctx.send("Seems something broke...\nwould you mind to tell my owner :)")
