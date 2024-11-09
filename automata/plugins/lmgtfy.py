import urllib.parse

from discord.ext import commands

from automata.utils import CommandContext


class LMGTFY(commands.Cog):
    """Create a LMGTFY link, for people who should have google'd first"""

    @commands.command()
    async def lmgtfy(self, ctx: CommandContext, *, search_terms: str):
        """Creates a LMGTFY link with the given search terms"""

        search_terms = urllib.parse.quote(search_terms)
        url = f"http://lmgtfy.com/?q={search_terms}"

        await ctx.send(url)
