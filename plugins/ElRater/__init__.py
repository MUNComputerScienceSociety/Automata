from nextcord.ext import commands

from Plugin import AutomataPlugin

import random


class Dice(AutomataPlugin):
    """Rolls two 6-sided dices"""

    @commands.command()
    async def dice(self, ctx: commands.Context):
        """Replies with two numbers, rolled between 1 and 6"""
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        await ctx.send(f"Your numbers are {a} and {b}")
