import discord
import httpx
from discord.ext import commands

from Plugin import AutomataPlugin

API_BASE = "http://yerkee.com/api"


class FortuneCookie(AutomataPlugin):
    """A fortune cookie"""

    @staticmethod
    async def _fetch(api_path):
        async with httpx.AsyncClient() as client:
            return await client.get(f"{API_BASE}{api_path}")

    @commands.command()
    async def fortune(self, ctx: commands.Context):
        """Replies with a fortune cookie message"""

        response = await self._fetch("/fortune/computers")
        text = response.json()["fortune"]
        if len(text) > 1024:
            text = "I am too long"
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name="Your Fortune Cookie 🥠", value=text)
        message = await ctx.send(embed=embed)
        await message.add_reaction("🥠")
