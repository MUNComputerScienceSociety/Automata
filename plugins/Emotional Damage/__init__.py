from nextcord.ext import commands
from Plugin import AutomataPlugin
import random

GIF_ONE = "https://leahhynes.github.io/EmotionalDamage/1.gif"
GIF_TWO = "https://leahhynes.github.io/EmotionalDamage/2.gif"
GIF_THREE = "https://leahhynes.github.io/EmotionalDamage/3.gif"


class Damage(AutomataPlugin):
    """Emotional Damage"""

    @commands.command()
    async def damage(self, ctx: commands.Context):
        """Replies with a randomized gif of Stephen He saying Emotional Damage"""

        gifint = random.randint(1, 3)
        if gifint == 1:
            await ctx.send(GIF_ONE)
        elif gifint == 2:
            await ctx.send(GIF_TWO)
        elif gifint == 3:
            await ctx.send(GIF_THREE)
