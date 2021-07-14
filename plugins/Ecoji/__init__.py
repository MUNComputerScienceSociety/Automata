import requests
from discord.ext import commands
from Plugin import AutomataPlugin

URANDOM_ECOJI_URI = "https://jackharrhy.dev/urandom/ecoji/"
MIN = 1
MAX = 400


class Ecoji(AutomataPlugin):
    """Sends randomly generated emojis from https://github.com/jackharrhy/DUaaS"""

    @commands.command()
    async def ecoji(self, ctx: commands.Context, amount=MIN):
        """Replies with random emojis, amount defaults to 1, and can be set up to 400"""

        if amount < MIN:
            await ctx.send(f"Amount must be greater than {MIN - 1}")
        elif amount > MAX:
            await ctx.send(f"Amount must be less than than {MAX + 1}")
        else:
            await ctx.send(requests.get(f"{URANDOM_ECOJI_URI}{amount}").text)
