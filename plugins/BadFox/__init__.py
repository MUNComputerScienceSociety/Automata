from nextcord.ext import commands

from Plugin import AutomataPlugin


class BadFox(AutomataPlugin):
    """Asks if I'm really a bad fox"""

    @commands.command()
    async def BadFox(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a Am_I_really_a_BadFox? :confused: ), or many!"""

        if number_of_times == 0:
            await ctx.send("Am_I_really_a_BadFox? :confused:")
        else:
            await ctx.send(f"Am_I_really_a_BadFox? :confused: x{number_of_times}")

        