from discord.ext import commands

from Plugin import AutomataPlugin

import random

class Coinflip(AutomataPlugin):
    """Literally a coin flip!"""

    @commands.command()
    async def coinflip(self, ctx: commands.Context, number_of_times: int = 1):
        """Flips the coin n times!"""

        for i in range(number_of_times):
            flip = random.randint(0,1)
            if(flip == 0):
                await ctx.send("Heads!")
            else:
                await ctx.send("Tails!")


