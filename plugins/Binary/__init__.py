from nextcord.ext import commands

from Plugin import AutomataPlugin

class Binary(AutomataPlugin):
    """Binary"""

    @commands.command()
    async def binary(self, ctx: commands.Context, message: str):
        binaryString = ""

        for char in message:
            binaryString += format(ord(char), 'b') + " "

        await ctx.send(binaryString)
