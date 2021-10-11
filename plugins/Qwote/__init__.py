import httpx
import json, random
from nextcord.ext import commands
from Plugin import AutomataPlugin

QUOTES_ENDPOINT = "https://type.fit/api/quotes"


class Qwote(AutomataPlugin):
    """Qwotes"""

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.quotes = json.loads(httpx.get(QUOTES_ENDPOINT).text)

    @commands.command()
    async def qwote(self, ctx):
        """qwote uwu"""

        quote = random.choice(self.quotes)
        response = '"{text}" -**{author}**'

        formatted = response.format(
            text=quote["text"],
            author=quote["author"]
            if "author" in quote.keys() and quote["author"] != None
            else "Unknown",
        )

        transform = (
            formatted.lower().replace("r", "w").replace("l", "w").replace("n", "ny")
        )
        await ctx.send(transform)
