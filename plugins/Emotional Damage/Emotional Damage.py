from nextcord.ext import commands
from Plugin import AutomataPlugin
import random

class Damage(AutomataPlugin):
    """Emotional Damage"""
    
    @commands.command()
    async def damage(self, ctx: commands.Context):
        """Replies with a randomized gif of Stephen He saying Emotional Damage"""

        gifint = random.randint(1,3)
        if gifint == 1:
            await ctx.send(file = discord.File('1.gif'))
        elif gifint == 2:
            await ctx.send(file = discord.File('2.gif'))
        elif gifint == 3:
            await ctx.send(file = discord.File('3.gif'))