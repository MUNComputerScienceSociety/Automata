from nextcord.ext import commands

from Plugin import AutomataPlugin

import random

class Dice(AutomataPlugin):
    """Pong"""

    @commands.command()
    async def dice(self, ctx: commands.Context):
        a = random.randint(1,6)
        b = random.randint(1,6)
        """Replies with a Pong, or many!"""
        await ctx.send(f"your numbers are {a} and {b}")

    @commands.command()
    async def minwage(self, ctx: commands.Context):
        a = random.randint(1,2)
        """Replies with a Pong, or many!"""
        await ctx.send(f"it is 12 canadian dolllars 50 cents")
        