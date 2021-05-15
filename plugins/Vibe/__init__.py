import discord
from discord.ext import commands

from Plugin import AutomataPlugin

VIBE_IMAGE = "https://s3.gifyu.com/images/catvibe.gif"
VIBIER_IMAGE = ""
VIBIEST_IMAGE = ""

class Vibe(AutomataPlugin):
    """Cat Bop"""

    @commands.command()
    async def vibe(self, ctx: commands.Context, vibelevel: int = 1):
        """Replies with a Cat Bop Gif! Vibe level can also be specified."""
        if vibelevel == 1:
            await ctx.send(VIBE_IMAGE)
        elif vibelevel == 2:
            await ctx.send(VIBIER_IMAGE)
        else:
            await ctx.send(VIBIEST_IMAGE)
