import discord
from discord.ext import commands

from Plugin import AutomataPlugin
from Globals import DISABLED_PLUGINS


class Ping(AutomataPlugin):
    """Pong"""

    def __init__(self, manifest, bot):
        if not self.__class__.__name__ in DISABLED_PLUGINS:
            super().__init__(manifest, bot)

    @commands.command()
    async def ping(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a Pong, or many!"""

        if number_of_times == 0:
            await ctx.send("Pong!")
        else:
            await ctx.send(f"Pong! x{number_of_times}")
