from nextcord.ext import commands

from Plugin import AutomataPlugin


class Ping(AutomataPlugin):
    """Pong"""

    @commands.command()
    async def ping(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a Pong, or many!"""

        if number_of_times == 0:
            await ctx.send("EVIL JACK BE LIKE PONG")
        else:
            await ctx.send(f"Pong! x{number_of_times}")
