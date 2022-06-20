import urllib.parse

from discord.ext import commands
import discord
import httpx

from Plugin import AutomataPlugin

COWSAY_API = "https://cowsay.morecode.org/say"


class Cowsay(AutomataPlugin):
    """
    Cowsay
    Made using https://cowsay.morecode.org/
    """

    @commands.command()
    async def cowsay(self, ctx: commands.Context, message: str):
        """Responds with a cow, saying your message"""

        cow = httpx.get(COWSAY_API, params={"message": message, "format": "text"}).text

        message = await ctx.send(f"```{cow}```")
        await message.add_reaction("🐮")
