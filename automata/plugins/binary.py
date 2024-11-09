from discord.ext import commands

from automata.utils import CommandContext, Plugin


class Binary(Plugin):
    """Binary"""

    @commands.command()
    async def binary(self, ctx: CommandContext, message: str):
        binaryString = ""

        for char in message:
            binaryString += format(ord(char), "b") + " "

        await ctx.send(binaryString)
