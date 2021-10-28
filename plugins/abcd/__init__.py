from nextcord.ext import commands

from Plugin import AutomataPlugin


class abcd(AutomataPlugin):
    """Pong"""

    @commands.command()
    async def abcd(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a efgh, or many!"""

        if number_of_times == 0:
            await ctx.send("efgh!")
        else:
            await ctx.send(f"efgh! x{number_of_times}")
