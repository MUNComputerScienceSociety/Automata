import nextcord
from nextcord.ext import commands

from Plugin import AutomataPlugin

VIBE_IMAGE = "https://s3.gifyu.com/images/catvibe.gif"
VIBIER_IMAGE = "https://s3.gifyu.com/images/ezgif.com-gif-maker-174e18faa852a3028.gif"
VIBIEST_IMAGE = "https://s3.gifyu.com/images/ezgif.com-gif-maker-2664260aedaea9638.gif"
NO_VIBE = "https://s6.gifyu.com/images/ezgif.com-gif-maker682fded14a604d26.gif"


class Vibe(AutomataPlugin):
    """Cat Bop"""

    @commands.command()
    async def vibe(self, ctx: commands.Context, vibelevel: int = 1):
        """Replies with a Cat Bop Gif! Vibe levels from 1-3 can also be specified."""
        if vibelevel <= 0:
            await ctx.send(NO_VIBE)
        elif vibelevel == 1:
            await ctx.send(VIBE_IMAGE)
        elif vibelevel == 2:
            await ctx.send(VIBIER_IMAGE)
        else:
            await ctx.send(VIBIEST_IMAGE)
