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
        ecojiTxt = self.fetch_ecoji_emotes(limit)
        for row in ecojiTxt:
            ecojiRows = row.decode("utf-8")
            await ctx.send(ecojiRows)

    def fetch_ecoji_emotes(self, limit):
        return requests.get(URANDOM_ECOJI_URI + str(limit))
