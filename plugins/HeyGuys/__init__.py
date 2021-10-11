from nextcord.ext import commands

from Plugin import AutomataPlugin


class HeyGuys(AutomataPlugin):
    """Someone to say hey guys when you're lonely"""

    @commands.command()
    async def heyguys(self, ctx: commands.Context):
        """Bot will say hey guys back"""

        await ctx.send("Hey Guys")
