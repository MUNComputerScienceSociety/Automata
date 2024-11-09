from discord.ext import commands

from Plugin import AutomataPlugin

VIBE_IMAGE = "https://hamzahap.github.io/VibeGIFS/Vibe.gif"
VIBIER_IMAGE = "https://hamzahap.github.io/VibeGIFS/HyperVibe.gif"
VIBE_CAR = "https://hamzahap.github.io/VibeGIFS/Vibey.gif"
NO_VIBE = "https://hamzahap.github.io/VibeGIFS/Cry.gif"


class Vibe(AutomataPlugin):
    """Cat Bop"""

    @commands.command()
    async def vibe(self, ctx: commands.Context, vibelevel: int = 1):
        """Replies with a Cat Bop Gif! Vibe levels from 1-3 can also be specified."""
        if vibelevel <= 0:
            await ctx.send(NO_VIBE)
        elif vibelevel == 1:
            await ctx.send(VIBE_IMAGE)
        elif vibelevel == 69 or vibelevel == 420:
            await ctx.send(VIBE_CAR)
        else:
            await ctx.send(VIBIER_IMAGE)
