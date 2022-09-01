from discord.ext import commands

from Plugin import AutomataPlugin


class PingFlags(commands.FlagConverter):
    number_of_times: int = commands.flag(default=0, description='The number of Pong replies!')

class Ping(AutomataPlugin):
    """Pong"""

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context, flags: PingFlags):
        """Replies with a Pong, or many!"""

        if flags.number_of_times == 0:
            await ctx.send("Pong!")
        else:
            await ctx.send(f"Pong! x{flags.number_of_times}")

