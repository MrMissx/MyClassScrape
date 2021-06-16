"""Bot decorators."""

from functools import wraps


def send_typing(coro):
    """Send typing status while processing the commands."""

    @wraps(coro)
    async def command_func(ctx, *args, **kwargs):
        await ctx.trigger_typing()
        return await coro(ctx, *args, **kwargs)

    return command_func


def check_nsfw(coro):
    """Check if a channel was NSFW."""

    @wraps(coro)
    async def check(ctx, *args, **kwargs):
        if not ctx.guild or ctx.message.channel.nsfw:
            return await coro(ctx, *args, **kwargs)
        else:
            return await ctx.reply(
                "You can only use this command in NSFW channel!",
                delete_after=5
            )

    return check
