import discord
import requests
from discord.ext import commands
from Plugin import AutomataPlugin

URANDOM_ECOJI_URI = "https://jackharrhy.dev/urandom/ecoji/"


class Ecoji(AutomataPlugin):
    f"""Sends randomly generated emojis from {URANDOM_ECOJI_URI}"""

    @commands.command()
    async def ecoji(self, ctx: commands.Context, limit):
        await ctx.send(requests.get(f"{URANDOM_ECOJI_URI}{limit}").text)
