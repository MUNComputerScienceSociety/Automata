import urllib.parse

from nextcord.ext import commands
import nextcord
import httpx

from Plugin import AutomataPlugin


API = "https://awful-3x3-meme-generator.herokuapp.com/api"


class Generator(AutomataPlugin):
    """
    Generates a meme that's probably already dead
    """

    @commands.command()
    async def gen3x3(
        self,
        ctx: commands.Context,
        lawful_good,
        neutral_good,
        chaotic_good,
        lawful_neutral,
        true_neutral,
        chaotic_neutral,
        lawful_evil,
        neutral_evil,
        chaotic_evil,
    ):
        """Responds with a meme that's probably already dead"""

        params = {
            "lg": lawful_good,
            "ng": neutral_good,
            "cg": chaotic_good,
            "ln": lawful_neutral,
            "tn": true_neutral,
            "cn": chaotic_neutral,
            "le": lawful_evil,
            "ne": neutral_evil,
            "ce": chaotic_evil,
        }

        await ctx.send(f"{API}?{urllib.parse.urlencode(params)}")
