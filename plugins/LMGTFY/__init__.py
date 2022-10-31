import urllib
import discord
from discord.ext import commands

from Plugin import AutomataPlugin


class LMGTFY(AutomataPlugin):
    """Create a LMGTFY link, for people who should have google'd first"""

    @commands.command()
    async def lmgtfy(self, ctx: commands.Context, *, search_terms: str):
        """Creates a LMGTFY link with the given search terms"""

        search_terms = urllib.parse.quote(search_terms)
        url = f"http://lmgtfy.com/?q={search_terms}"

        await ctx.send(url)
