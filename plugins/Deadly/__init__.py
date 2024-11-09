from discord.ext import commands
from Plugin import AutomataPlugin


# Leigh Trinity
# Oct 12th 2021
class Deadly(AutomataPlugin):
    """deadly"""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

    @commands.command()
    async def deadly(self, ctx: commands.Context, number_of_times: int = 0):
        if number_of_times == 0:
            await ctx.send("yes by!")
        else:
            await ctx.send(f"yes by'! x{number_of_times}")
