from functools import wraps


def send_typing(coro):
    """Send typing status while processing the commands."""

    @wraps(coro)
    async def command_func(ctx, *args, **kwargs):
        await ctx.trigger_typing()
        return await coro(ctx, *args, **kwargs)

    return command_func
