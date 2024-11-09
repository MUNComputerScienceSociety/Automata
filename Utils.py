import io

import discord


async def send_code_block_maybe_as_file(ctx, text):
    """
    Sends a code block to the current context.

    If it's too long to fit in a single message, it will
    instead be sent as a file.
    """
    if len(text) > 2000:
        file = io.StringIO()
        file.writelines(text)
        file.seek(0)

        await ctx.send(file=discord.File(file, filename="agenda.md"))
    else:
        await ctx.send(f"```{text}```")
