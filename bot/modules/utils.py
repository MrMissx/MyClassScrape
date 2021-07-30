import io
import os
import requests

from discord import File

from bot import bot, REM_BG_API_KEY


@bot.command(aliases=["remove_bg"])
async def rbg(ctx, link: str = None):
    """For .rbg command, Remove Image Background."""
    if REM_BG_API_KEY is None:
        await ctx.send("Can't use this command... Please contact my owner")
        return
    msg = await ctx.send("Processing...")
    if ctx.message.reference:
        reply_img = ctx.message.reference.resolved.attachments
        if not reply_img:
            await msg.edit(content="Reply to an image!")
        reply_img = reply_img[0]
        if "image" in reply_img.content_type.split("/"):
            filename = reply_img.filename
            file = await reply_img.save(filename)
            removed = await rm_file(filename)
            os.remove(filename)
        else:
            return await msg.edit(content="How do I remove the background from this ?", delete_after=4)
    elif link:
        await msg.edit(
            content=f"Removing background from online image hosted at\n<{link}>")
        removed = await rm_url(link)
    else:
        await msg.edit(content="I need something to remove the background from.")
        return
    content_type = removed.headers.get("content-type")
    if "image" in content_type.split("/"):
        with io.BytesIO(removed.content) as remove_bg_image:
            remove_bg_image.name = "removed_bg.png"
            file = File(remove_bg_image)
            await ctx.reply(file=file)
            await msg.delete()
    else:
        await msg.edit(content="**Error (Invalid API key, I guess ?)**\n`{}`".format(
            removed.content.decode("UTF-8")))


async def rm_file(input_file_name):
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers={"X-API-Key": REM_BG_API_KEY,},
        files={"image_file": (input_file_name, open(input_file_name, "rb")),},
        allow_redirects=True,
        stream=True
    )


async def rm_url(input_url):
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers={"X-API-Key": REM_BG_API_KEY},
        data={"image_url": input_url},
        allow_redirects=True,
        stream=True
    )