from discord.ext import commands

from Plugin import AutomataPlugin


class FRSTT(AutomataPlugin):
    """Yoo"""

    @commands.command()
    async def FRSTT(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a yoo, or many!"""

        if number_of_times == 0:
            await ctx.send("yoo")
        else:
            await ctx.send(f"yoo x{number_of_times}")
