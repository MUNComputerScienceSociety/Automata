import httpx
import json, random
from nextcord.ext import commands
from Plugin import AutomataPlugin

QUOTES_ENDPOINT = "https://type.fit/api/quotes"


class WiseQuote(AutomataPlugin):
    """Quotes from wise people"""

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.quotes = json.loads(httpx.get(QUOTES_ENDPOINT).text)

    @commands.command()
    async def wisequote(self, ctx):
        """Replies with a quote from a wise person"""

        quote = random.choice(self.quotes)
        response = '"{text}" -**{author}**'
        await ctx.send(
            response.format(
                text=quote["text"],
                author=quote["author"]
                if "author" in quote.keys() and quote["author"] != None
                else "Unknown",
            )
        )
