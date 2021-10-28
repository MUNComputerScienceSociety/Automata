from nextcord.ext import commands

from Plugin import AutomataPlugin


class robotcheck(AutomataPlugin):
    """robotcheck"""

    @commands.command()
    async def robotcheck(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a no!, or many!"""

        if number_of_times == 0:
            await ctx.send("are you a robot?")
        else:
            await ctx.send(f"no! x{number_of_times}")
