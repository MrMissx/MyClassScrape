import re
import sys
import asyncio
from getpass import getuser

from discord.ext import commands

from bot import bot
from bot.utils import send_typing


@bot.command(aliases=["eval"])
@send_typing
async def evaluate(ctx, *, expression: str = None):
    if not expression:
        if ctx.message.reference:  # if reply to an expression
            expression = ctx.message.reference.resolved.content
        else:
            return await ctx.send("Give me some expression to evaluate!")
    expression = await parse_text(expression.strip())
    if await check_expresison(ctx, expression):
        return await ctx.send(
            "**Unpermitted import!**\n"
            "Your expresison contain sensitive method to me."
            "Only my owner can do that")
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        '-c',
        expression.strip(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

    result = None
    if stdout:
        result = f"**[stdout]**\n```{stdout.decode().strip()}```"
    if stderr:
        result = f"**[stderr]**\n```{stderr.decode().strip()}```"

    if result:
        await ctx.send(result)
    else:
        await ctx.send("Expression result is False/None")


@commands.is_owner()
@bot.command(aliases=["term"])
@send_typing
async def terminal(ctx, *, command: str = None):
    """Owner only commands."""
    if not command:
        if ctx.message.reference:  # if reply to a command
            command = ctx.message.reference.resolved.content
        else:
            return await ctx.send("Give me some command to execute!")
    command = await parse_text(command.strip())
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    user = getuser() + "@" + str(bot.user.name)
    await ctx.send(f"```{user}:~$ {command} \n{result}```")


async def check_expresison(ctx, text) -> bool:
    """ Check sensitive expression """
    app = await bot.application_info()
    if ctx.author.id == app.owner.id:
        return False  # Owner can do everything

    match = re.search(r"(from|import) (bot|os)|SAVED_SECRET", text)
    return bool(match)


async def parse_text(raw_text) -> str:
    """ Remove codeblock """
    text = re.sub(r"(^`{1,3}[a-zA-Z]*\n|`{1,3}$)", "", raw_text)  # remove codeblock if exist
    return text.strip()
