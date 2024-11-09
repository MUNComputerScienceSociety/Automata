import discord
from discord.ext import commands

from Plugin import AutomataPlugin


class Halal(AutomataPlugin):
    """Democratic version of asking Hking"""

    @commands.command()
    async def halal(self, ctx: commands.Context):
        """Asks if item is Halal"""
        message = ctx.message.content
        item = discord.utils.escape_mentions(message[7:])
        if len(item) < 1:
            item = f"<@{ctx.message.author.id}>"
        msg = await ctx.send(f"Is {item} halal?")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
