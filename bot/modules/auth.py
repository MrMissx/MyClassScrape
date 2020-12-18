"""Auth new user to database."""

import discord

from bot import bot, BOT_PREFIX
from bot.utils import encrypt, get_collection, send_typing


SAVED_SECRET = get_collection("CREDATA")


@bot.command(aliases=["save"])
@send_typing
async def auth(ctx, cred: str = None):
    """Authenticate new user."""
    author = ctx.author

    if cred is None:  # if no credential given
        text = (
            f"`{BOT_PREFIX}auth <username>$<password>`"
            "\n\n*username without @binus.ac.id*"
            "\n\n**disclaimer:** This bot doesn't save any of your credentials! "
            "It only get the message_id and encrypt it. As long as the message isn't "
            f"deleted you can use `{BOT_PREFIX}getclass` command. To delete your "
            f"credential just delete your {BOT_PREFIX}auth..... message")

        embed = discord.Embed(
            color=0x9B59B6,
            description=text,
            title="**Please enter your credential with this format**",
        )
        await author.send(embed=embed)
        if ctx.guild is not None:  # dont send if in PM's
            await ctx.send("I've send the help on PM's :)")
        return

    try:  # just checking the format
        cred.replace(f"{BOT_PREFIX}auth ", "")
        _, _ = cred.split("$")
    except ValueError:
        await ctx.send("Please send your credential like the format given")
        return

    msg_id = ctx.message.id
    saved = await SAVED_SECRET.find_one({"_id": str(author.id)})
    if saved is None:  # new data
        await SAVED_SECRET.insert_one(
            {"_id": str(author.id), "secret": encrypt(str(msg_id))}
        )
    else:  # update
        await SAVED_SECRET.find_one_and_update(
            {"_id": str(author.id)}, {"$set": {"secret": encrypt(str(msg_id))}}
        )
    await ctx.send("Saved\nTo delete your credentials just delete the message i react with \u2705")
    await ctx.message.add_reaction("\u2705")
