import asyncio
import io
import re
import sys
import traceback
from getpass import getuser

from discord.ext import commands

from bot import bot
from bot.utils import send_typing

from .webtools import push_dogbin


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
    if stderr:
        result = f"**[stderr]**\n```\n{stderr.decode().strip()}\n```"
    if stdout:
        result = f"**[stdout]**\n```\n{stdout.decode().strip()}\n```"

    if not result or len(result) < 2000:
        await ctx.reply(result if result else "Expression result is False/None")
    else:
        msg = await ctx.reply("Result too long... Pasting to Nekobin!")
        url =await push_dogbin(str(result))
        if not url:
            return await msg.edit(content="Failed to reach Nekobin")
        await msg.edit(content=url)

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
    await ctx.reply(f"```{user}:~$ {command} \n{result}```")


@commands.is_owner()
@bot.command(aliases=["exec"])
@send_typing
async def execute(ctx, *, expression: str = None):
    if not expression:
        if ctx.message.reference:  # if reply to an expression
            expression = ctx.message.reference.resolved.content
        else:
            return await ctx.send("Give me some expression to evaluate!")
    expression = await parse_text(expression.strip())

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        returned = await aexec(ctx, expression)
    except Exception:  # pylint: disable=broad-except
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue().strip()
    stderr = redirected_error.getvalue().strip()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    result = str(exc or stderr or stdout or returned).strip()
    if not result:
        return
    result = f"**[Result]**\n```{result}```"
    if len(result) < 2000:
        await ctx.reply(result)
    else:
        msg = await ctx.reply("Result too long... Pasting to Nekobin!")
        url =await push_dogbin(str(exc or stderr or stdout or returned).strip())
        if not url:
            return await msg.reply(content="Failed to reach Nekobin")
        await msg.edit(content=url)

async def aexec(ctx, code):
    """execute command"""
    head = "async def __aexec(ctx):\n "
    code = "".join((f"\n {line}" for line in code.split("\n")))
    exec(head + code)  # pylint: disable=exec-used
    return await locals()["__aexec"](ctx)


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
