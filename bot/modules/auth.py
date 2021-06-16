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
            "\ne.g: MyClassScraper$12345678"
            "\n\n**disclaimer:** This bot doesn't save any of your username nor password! "
            "It only get your credentials (user_id and message_id) then encrypt it. "
            "As long as the message isn't deleted you can use the scraping command. "
            "To delete that saved data, "
            f"just delete your {BOT_PREFIX}auth message or simply type `{BOT_PREFIX}unauth`")

        embed = discord.Embed(
            color=0x9B59B6,
            description=text,
            title="**Please enter your credential with this format**",
        )
        await author.send(embed=embed)
        if ctx.guild is not None:  # dont send if in PM's
            await ctx.reply(
                "This command only available on PMs!\nI've send help on your PM.",
                delete_after=5,
            )
        return

    try:  # just checking the format
        cred.replace(f"{BOT_PREFIX}auth ", "")
        raw = cred.split("$")
        if len(raw) > 2:  # Handle if password contains separator character
            _ = raw[0]
            _ = "$".join(raw[1:])
        else:
            _, _ = raw
    except ValueError:
        await ctx.send("Please send your credential like the format given")
        return

    msg_id = ctx.message.id
    await SAVED_SECRET.update_one(
        {"_id": str(author.id)},
        {"$set": {"secret": encrypt(str(msg_id))}},
        upsert=True
    )
    await ctx.reply("Saved\nTo delete your credentials just delete the message i reply")
    await ctx.message.add_reaction("\u2705")


@bot.command(aliases=["gdpr"])
@send_typing
async def unauth(ctx):
    """Delete user credentials"""
    author = ctx.author
    data = await SAVED_SECRET.find_one_and_delete(
        {'_id': str(author.id)}
    )
    if data:
        await ctx.reply("Done...\nYour credentials have been deleted")
    else:
        await ctx.reply("You haven't authenticate any credentials!")
