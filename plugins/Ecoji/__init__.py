import json

import discord
import requests
from discord.ext import commands

URANDOM_ECOJI_URI = "https://jackharrhy.dev/urandom/ecoji/"


from Plugin import AutomataPlugin


class Ecoji(AutomataPlugin):
    """Sends randomly generated emojis from Jack Harrhy's Ecoji project"""

    @commands.command()
    async def ecoji(self, ctx: commands.Context, limit):
        await ctx.send(requests.get(f"{URANDOM_ECOJI_URI}{limit}").text)
