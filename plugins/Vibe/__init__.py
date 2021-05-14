import discord
from discord.ext import commands

from Plugin import AutomataPlugin


class Vibe(AutomataPlugin):
    """Cat Bop"""

    @commands.command()
    async def vibe(self, ctx: commands.Context):
        """Replies with a Cat Bop Gif!"""

        await ctx.send("https://imgur.com/a/pKwXAH5")
