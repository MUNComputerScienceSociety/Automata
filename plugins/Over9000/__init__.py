from random import choice, randint
import discord
from discord.ext import commands

from .quotes import DBZQuotes

from Plugin import AutomataPlugin


class Over9000(AutomataPlugin):
    """Kakarot"""

    @commands.command()
    async def over9000(self, ctx: commands.Context, dbz_char: str = 'goku'):
        """Replies with a super saiyan emoji and random
        Goku quote!

        Takes character name as an argument.

        """


        dbz_quotes = DBZQuotes()

        if dbz_char.upper() in ('GOKU', 'KAKAROT'):
            quotes = dbz_quotes.goku()
            quote = choice(quotes)
            await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n**Goku:** {quote}")

        elif dbz_char.upper() == 'FRIEZA':
            quotes = dbz_quotes.frieza()
            quote = choice(quotes)
            await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n**Frieza:** {quote}")
        
        elif dbz_char.upper() == 'VEGETA':
            quotes = dbz_quotes.vegeta()
            quote = choice(quotes)
            await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n**Vegeta:** {quote}")

        else:
            """An invalid DBZ character was specified."""
            await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n...")
