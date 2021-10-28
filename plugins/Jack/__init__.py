from nextcord.ext import commands

from Plugin import AutomataPlugin



class Jack(AutomataPlugin):
    """Pong"""

    @commands.command()
    async def jack(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a Jack, or many!"""

        if number_of_times == 0:
            await ctx.send("Jack!")
        else:
            await ctx.send(f"Jack! x{number_of_times}")
