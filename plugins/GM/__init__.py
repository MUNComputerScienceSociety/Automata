from nextcord.ext import commands

from Plugin import AutomataPlugin


class GM(AutomataPlugin):
    """gm"""

    @commands.command()
    async def gm(self, ctx: commands.Context):
        """gm"""
        await ctx.send("gm")
