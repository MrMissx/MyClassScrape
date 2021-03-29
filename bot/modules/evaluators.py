import re
import sys
import asyncio

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
    if await check_expresison(expression):
        return await ctx.send("**Unpermitted import!**")
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        '-c',
        expression.strip(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    if result:
        await ctx.send(f"```\n{result}\n```")  # send as codeblock
    else:
        await ctx.send("Expression returned False/None")


async def check_expresison(text) -> bool:
    """ Check sensitive expression """
    match = re.search(r"(from|import) (bot|os)|SAVED_SECRET", text)
    return bool(match)


async def parse_text(raw_text) -> str:
    """ Remove codeblock """
    text = re.sub(r"(^`{1,3}[a-zA-Z]*\n|`{1,3}$)", "", raw_text)  # remove codeblock if exist
    return text.strip()
