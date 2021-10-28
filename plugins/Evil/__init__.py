from nextcord.ext import commands
from Plugin import AutomataPlugin

class Evil(AutomataPlugin):
    """Makes things Evil"""

    @commands.command()
    async def evil(self, ctx: commands.Context):
        """Reverses the last message of input user"""
        mentions = ctx.message.mentions
        if len(mentions) == 1:
            egassem_live = ctx.message.content.split('>', 1)[1][::-1]
            await ctx.send(f"EVIL {mentions[0].name} BE LIKE: {egassem_live}")
        elif len(mentions) > 1:
            await ctx.send("Too many mentions.")
        else:
            await ctx.send("Please mention someone.")
