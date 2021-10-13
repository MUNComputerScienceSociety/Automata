from nextcord.ext import commands

from Plugin import AutomataPlugin

import random

MAXIMUM_FLIPS = 5
MINIMUM_FLIPS = 1


class Coinflip(AutomataPlugin):
    """Literally a coin flip!"""

    @commands.command()
    async def coinflip(self, ctx: commands.Context, number_of_times: int = 1):
        """Flips the coin n times!"""
        if number_of_times <= MAXIMUM_FLIPS and number_of_times >= MINIMUM_FLIPS:
            for i in range(number_of_times):
                flip = random.randint(0, 1)
                if flip == 0:
                    await ctx.send("Heads!")
                else:
                    await ctx.send("Tails!")
        else:
            await ctx.send(
                f"Too many flips to handle, try less than {MAXIMUM_FLIPS + 1} and more than {MINIMUM_FLIPS - 1}!"
            )
