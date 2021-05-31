import discord
from discord.ext import commands

from Plugin import AutomataPlugin

class Hewwo(AutomataPlugin):
    """hewwo thewe, this wiww make youw wife cutew"""

    @commands.command()
    async def hewwo(self, ctx: commands.Context, *, arg):
        transform = arg.lower().replace('r', 'w').replace('l', 'w').replace('n', 'ny')
        await ctx.send(transform)
