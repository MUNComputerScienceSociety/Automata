from json import load
from os import path
from random import choice

from discord.ext import commands

from Plugin import AutomataPlugin


class Over9000(AutomataPlugin):
    """Kakarot"""

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)

        with open(path.join(self.manifest["path"], "quotes.json"), "r") as f:
            self.dbz_quotes = load(f)

    @commands.command()
    async def over9000(self, ctx: commands.Context, dbz_char: str = "goku"):
        """Replies with a super saiyan emoji and random
        Goku/Vegeta/Frieza quote.

        Takes character name as an argument.
        """

        if dbz_char.upper() in ("GOKU", "KAKAROT"):
            await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n**Goku:** {choice(self.dbz_quotes['goku'])}")

        elif dbz_char.upper() == "VEGETA":
            await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n**Vegeta:** {choice(self.dbz_quotes['vegeta'])}")

        elif dbz_char.upper() == "FRIEZA":
            await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n**Frieza:** {choice(self.dbz_quotes['frieza'])}")

        else:
            #  An invalid DBZ character was specified.
            await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n...")
